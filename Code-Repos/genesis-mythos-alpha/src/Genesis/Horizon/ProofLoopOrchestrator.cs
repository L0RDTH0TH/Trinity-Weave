using Genesis.Agency;
using Genesis.Boundary;
using Genesis.Core;
using Genesis.Perspective;
using Genesis.Rules;
using Genesis.Sim;
using Genesis.Ui;
using Godot;
using Godot.Collections;

namespace Genesis.Horizon;

/// <summary>8-beat Horizon path as a short playable session fragment (game language, not harness ids).</summary>
public sealed class SessionFlowDirector
{
	public const float ChapterDwellSeconds = 2.2f;

	public readonly record struct Chapter(string Id, string Title, string Body);

	public static readonly Chapter[] Chapters =
	{
		new("spawn", "Arrival", "You stand on the shrine path at dusk. The courtyard waits ahead."),
		new("fp_explore", "Explore", "Walk the path. Look around. This place is yours to feel."),
		new("intent", "Shared intent", "You reach toward the shrine — an intent takes shape."),
		new("sim", "The world turns", "One quiet tick: the living world answers your presence."),
		new("rule_check", "Rules speak", "A Pathfinder check settles against the shrine's DC."),
		new("dm_cam", "DM table view", "The table lifts — aerial mastery over the same courtyard."),
		new("overwrite", "Boundary holds", "A cross-track overwrite is refused. Seats matter."),
		new("feedback", "Session echo", "Feedback settles. The fragment ends — still placeholder, not a campaign ship."),
	};

	private PlayRegionHost? _host;
	private readonly System.Collections.Generic.Dictionary<string, ISessionBeat> _beats = new();
	public int CurrentIndex { get; private set; }
	public Chapter? CurrentChapter { get; private set; }
	public bool Complete { get; private set; }

	public System.Action<Chapter, int>? OnChapter { get; set; }

	public Error BindHost(PlayRegionHost host)
	{
		if (host == null) return Error.InvalidParameter;
		_host = host;
		return Error.Ok;
	}

	public Error BindBeat(string id, ISessionBeat beat)
	{
		if (string.IsNullOrEmpty(id) || beat == null) return Error.InvalidParameter;
		_beats[id] = beat;
		return Error.Ok;
	}

	public async System.Threading.Tasks.Task<Error> RunAsync(Node owner)
	{
		if (_host == null || !_host.IsMounted) return Error.Unconfigured;
		Complete = false;
		for (var i = 0; i < Chapters.Length; i++)
		{
			CurrentIndex = i + 1;
			CurrentChapter = Chapters[i];
			OnChapter?.Invoke(Chapters[i], CurrentIndex);
			if (!_beats.TryGetValue(Chapters[i].Id, out var beat))
				return Error.DoesNotExist;
			var err = beat.Run();
			if (err != Error.Ok) return err;
			var dwell = Chapters[i].Id == "fp_explore" ? 4.0f : ChapterDwellSeconds;
			await owner.ToSignal(owner.GetTree().CreateTimer(dwell), SceneTreeTimer.SignalName.Timeout);
		}
		Complete = true;
		return Error.Ok;
	}
}

public interface ISessionBeat
{
	Error Run();
}

public sealed class SpawnBeat : ISessionBeat
{
	private readonly PlayRegionHost _host;
	private readonly PresentationSessionHandle _handle;

	public SpawnBeat(PlayRegionHost host, PresentationSessionHandle handle)
	{
		_host = host;
		_handle = handle;
	}

	public Error Run()
	{
		if (!_host.IsMounted || _handle.SessionId == default) return Error.Unconfigured;
		return Error.Ok;
	}
}

public sealed class ExploreBeat : ISessionBeat
{
	private readonly CameraRigHost _cams;
	private readonly IAgencyEnvelope _agency;

	public ExploreBeat(CameraRigHost cams, IAgencyEnvelope agency)
	{
		_cams = cams;
		_agency = agency;
	}

	public Error Run()
	{
		var err = _agency.Assert(SeatContext.Player);
		if (err != Error.Ok) return err;
		err = _cams.Activate(PerspectiveMode.FirstPerson, SeatContext.Player);
		if (err != Error.Ok) return err;
		_cams.SetFpControl(true);
		return _cams.ApplyFov(75f);
	}
}

public sealed class IntentBeat : ISessionBeat
{
	public Dictionary LastIntent { get; private set; } = new();

	public Error Run()
	{
		LastIntent = new Dictionary
		{
			["kind"] = "intent_demo_interact",
			["target"] = "shrine_stele",
			["seat"] = "player",
		};
		return Error.Ok;
	}
}

public sealed class WorldTickBeat : ISessionBeat
{
	private readonly SimTickHost _sim;
	private readonly IntentBeat _intent;

	public WorldTickBeat(SimTickHost sim, IntentBeat intent)
	{
		_sim = sim;
		_intent = intent;
	}

	public Error Run()
	{
		if (!_intent.LastIntent.ContainsKey("kind")) return Error.Unconfigured;
		_sim.Arm();
		var err = _sim.Tick(1.0, new SimSnapshot { SimTime = 1.0 });
		if (err != Error.Ok) return err;
		var second = _sim.Tick(2.0, new SimSnapshot { SimTime = 2.0 });
		return second == Error.Bug ? Error.Ok : Error.Bug;
	}
}

public sealed class RulesBeat : ISessionBeat
{
	private readonly IRulesPluginHost _rules;
	public StringName Outcome { get; private set; } = new StringName();

	public RulesBeat(IRulesPluginHost rules) => _rules = rules;

	public Error Run()
	{
		if (_rules.ActiveRuleset.ToString() != "pathfinder_pf1") return Error.Unconfigured;
		var result = _rules.Evaluate(new CheckRequest
		{
			Mode = "check", Roll = "1d20", Modifier = 3, Dc = 10
		});
		Outcome = result.Outcome;
		var audit = _rules.Roll(DiceExpression.Parse("1d20+3"), RuleContextFrame.FromRulesSeed(42));
		return audit.Total < 1 ? Error.Bug : Error.Ok;
	}
}

public sealed class DmViewBeat : ISessionBeat
{
	private readonly CameraRigHost _cams;
	private readonly IAgencyEnvelope _agency;

	public DmViewBeat(CameraRigHost cams, IAgencyEnvelope agency)
	{
		_cams = cams;
		_agency = agency;
	}

	public Error Run()
	{
		_agency.Release("pilot_default");
		var err = _agency.Assert(SeatContext.DmAsPlayer);
		if (err != Error.Ok) return err;
		return _cams.Activate(PerspectiveMode.DmWorldCam, SeatContext.DmAsPlayer);
	}
}

public sealed class BoundaryBeat : ISessionBeat
{
	private readonly BuildProfileSelector _boundary;
	public Error LastRefuse { get; private set; }

	public BoundaryBeat(BuildProfileSelector boundary) => _boundary = boundary;

	public Error Run()
	{
		LastRefuse = _boundary.ProbeWrongTrackWrite();
		return LastRefuse == Error.Unauthorized ? Error.Ok : Error.Bug;
	}
}

public sealed class FeedbackBeat : ISessionBeat
{
	private readonly IUiHost _ui;

	public FeedbackBeat(IUiHost ui) => _ui = ui;

	public Error Run() => _ui.SetLayer("transient", true);
}
