using Genesis.Agency;
using Genesis.Core;
using Genesis.Exemplar;
using Genesis.Module;
using Genesis.Perspective;
using Genesis.Place;
using Genesis.Rules;
using Genesis.Seams;
using Genesis.Ui;
using Godot;

namespace Genesis.Table;

/// <summary>
/// Alpha 0 playable table fragment: load pack → FP in site → skill check → skirmish → DM rail + seat refuse.
/// </summary>
public partial class TablePlaySession : Node3D
{
	private ModulePack? _pack;
	private PregenCharacter? _pc;
	private EnemyDef? _enemy;
	private SeatId _activeSeat = SeatId.Player;
	private CameraRigHost? _cams;
	private RulesPluginHost? _rules;
	private AgencyEnvelope? _agency;
	private ReceiptLedger _ledger = new();
	private SiteDef? _site;

	private Label? _hudTitle;
	private Label? _hudBody;
	private Label? _hudSheet;
	private Label? _hudResult;
	private Label? _honesty;
	private Label? _controls;
	private Label? _toast;
	private ColorRect? _toastBg;
	private Label? _seatBadge;
	private Button? _skillBtn;
	private Button? _skirmishBtn;
	private Button? _attackBtn;
	private Button? _seatPlayerBtn;
	private Button? _seatDmBtn;
	private Button? _dmRailBtn;
	private Button? _backDoorBtn;
	private CanvasLayer? _hud;

	private bool _skillDone;
	private bool _skirmishStarted;
	private bool _skirmishOver;
	private bool _playerWinsInit;
	private ulong _rollSeed = 7;

	public event System.Action? ReturnToFrontDoor;

	public Error Start(ModulePack pack, SeatId initialSeat, string pregenId)
	{
		_pack = pack;
		_pc = pack.FindPregen(pregenId)?.CloneRuntime();
		if (_pc == null) return Error.DoesNotExist;
		_enemy = CloneEnemy(pack.Skirmish.Enemy);
		_activeSeat = initialSeat;
		_site = pack.FindSite(pack.DefaultSiteId) ?? pack.Sites[0];
		_skillDone = false;
		_skirmishStarted = false;
		_skirmishOver = false;
		_rollSeed = (ulong)Time.GetTicksMsec();

		ClearChildren();
		BuildHud();
		var err = MountTable();
		if (err != Error.Ok) return err;

		RefreshHud();
		ApplySeatCamera(showRefuseToast: false);
		// After role / front-door UI closes, release GUI focus so viewport gets look/move.
		CallDeferred(nameof(ReleaseUiFocusForPlay));
		return Error.Ok;
	}

	private void ReleaseUiFocusForPlay()
	{
		GetViewport()?.GuiReleaseFocus();
		if (_activeSeat == SeatId.Player || _cams?.ActiveMode == PerspectiveMode.FirstPerson)
			_cams?.CaptureMouseForFp();
	}

	private void ClearChildren()
	{
		foreach (var c in GetChildren())
			c.QueueFree();
		_cams = null;
		_hud = null;
	}

	private Error MountTable()
	{
		if (_pack == null || _site == null) return Error.Unconfigured;

		_ledger = new ReceiptLedger();
		var seams = new SeamRegistry();
		PublishRequiredSeams(seams);
		if (new CompletenessGate().Check(seams) != Error.Ok) return Error.Unavailable;

		var playRegion = new PlayRegionHost { Name = "PlayRegionHost" };
		playRegion.BindLedger(_ledger);
		AddChild(playRegion);

		var hudStack = new HUDLayerStack { Name = "HUDLayerStack" };
		hudStack.BindLedger(_ledger);
		AddChild(hudStack);

		var launch = new LaunchFlowController();
		launch.Bind(playRegion, hudStack);
		var shellErr = launch.RunWithDevLeakageGuard(_ledger);
		if (shellErr != Error.Ok) return shellErr;
		if (playRegion.PlayWorld == null) return Error.Unconfigured;

		ModuleSiteBuilder.Build(playRegion.PlayWorld, _site);

		_cams = new CameraRigHost { Name = "CameraRigHost" };
		_cams.BindLedger(_ledger);
		_cams.SetSpawnOrigin(_site.SpawnEye);
		_cams.SetDmOrigin(_site.DmEye);
		playRegion.BindSocket("camera_rig", _cams);

		_agency = new AgencyEnvelope();
		_agency.BindLedger(_ledger);

		_rules = new RulesPluginHost(new SeededDiceRoller(), seams);
		_rules.BindLedger(_ledger);
		if (_rules.BindPlugin(new PathfinderPf1Plugin()) != Error.Ok) return Error.Unavailable;

		_ledger.Record("R.module.pack_load", "placeholder_ok",
			$"pack_id={_pack.PackId};pregens={_pack.Pregens.Count};sites={_pack.Sites.Count}");

		return Error.Ok;
	}

	private void BuildHud()
	{
		_hud = new CanvasLayer { Name = "TableHud", Layer = 25 };
		AddChild(_hud);

		var panel = new PanelContainer
		{
			Position = new Vector2(24, 20),
			CustomMinimumSize = new Vector2(560, 130),
			// Do not eat viewport clicks needed for mouse recapture after Esc.
			MouseFilter = Control.MouseFilterEnum.Ignore,
		};
		var style = new StyleBoxFlat
		{
			BgColor = new Color(0.05f, 0.06f, 0.09f, 0.78f),
			CornerRadiusTopLeft = 6,
			CornerRadiusTopRight = 6,
			CornerRadiusBottomLeft = 6,
			CornerRadiusBottomRight = 6,
			ContentMarginLeft = 14,
			ContentMarginRight = 14,
			ContentMarginTop = 10,
			ContentMarginBottom = 10,
		};
		panel.AddThemeStyleboxOverride("panel", style);
		_hud.AddChild(panel);

		var vbox = new VBoxContainer { MouseFilter = Control.MouseFilterEnum.Ignore };
		panel.AddChild(vbox);

		_hudTitle = new Label { Text = "Table", MouseFilter = Control.MouseFilterEnum.Ignore };
		_hudTitle.AddThemeFontSizeOverride("font_size", 24);
		_hudTitle.AddThemeColorOverride("font_color", new Color(0.95f, 0.88f, 0.62f));
		vbox.AddChild(_hudTitle);

		_hudBody = new Label
		{
			Text = "",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
			CustomMinimumSize = new Vector2(520, 0),
			MouseFilter = Control.MouseFilterEnum.Ignore,
		};
		_hudBody.AddThemeFontSizeOverride("font_size", 14);
		_hudBody.AddThemeColorOverride("font_color", new Color(0.88f, 0.90f, 0.94f));
		vbox.AddChild(_hudBody);

		_hudSheet = new Label { Text = "", Position = new Vector2(24, 170), MouseFilter = Control.MouseFilterEnum.Ignore };
		_hudSheet.AddThemeFontSizeOverride("font_size", 13);
		_hudSheet.AddThemeColorOverride("font_color", new Color(0.75f, 0.9f, 0.8f));
		_hud.AddChild(_hudSheet);

		_seatBadge = new Label { Text = "", Position = new Vector2(24, 210), MouseFilter = Control.MouseFilterEnum.Ignore };
		_seatBadge.AddThemeFontSizeOverride("font_size", 14);
		_seatBadge.AddThemeColorOverride("font_color", new Color(0.85f, 0.82f, 0.55f));
		_hud.AddChild(_seatBadge);

		_honesty = new Label
		{
			Text = "Example module cartridge — NOT campaign ship / NOT full Genesis campaign. No LAN.",
			Position = new Vector2(24, 240),
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
			CustomMinimumSize = new Vector2(700, 0),
			MouseFilter = Control.MouseFilterEnum.Ignore,
		};
		_honesty.AddThemeFontSizeOverride("font_size", 12);
		_honesty.AddThemeColorOverride("font_color", new Color(0.62f, 0.66f, 0.55f));
		_hud.AddChild(_honesty);

		_hudResult = new Label
		{
			Text = "",
			Position = new Vector2(24, 280),
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
			CustomMinimumSize = new Vector2(720, 0),
			MouseFilter = Control.MouseFilterEnum.Ignore,
		};
		_hudResult.AddThemeFontSizeOverride("font_size", 16);
		_hudResult.AddThemeColorOverride("font_color", new Color(0.95f, 0.92f, 0.75f));
		_hud.AddChild(_hudResult);

		_toastBg = new ColorRect
		{
			Color = new Color(0.5f, 0.06f, 0.06f, 0.9f),
			Position = new Vector2(24, 360),
			Size = new Vector2(680, 48),
			Visible = false,
		};
		_hud.AddChild(_toastBg);
		_toast = new Label
		{
			Text = "",
			Position = new Vector2(36, 370),
			Visible = false,
		};
		_toast.AddThemeFontSizeOverride("font_size", 20);
		_toast.AddThemeColorOverride("font_color", new Color(1f, 0.5f, 0.5f));
		_hud.AddChild(_toast);

		var actions = new HBoxContainer
		{
			Position = new Vector2(24, 430),
		};
		actions.AddThemeConstantOverride("separation", 10);
		_hud.AddChild(actions);

		_skillBtn = new Button { Text = "Skill check", CustomMinimumSize = new Vector2(140, 36), FocusMode = Control.FocusModeEnum.None };
		_skillBtn.Pressed += RunSkillCheck;
		actions.AddChild(_skillBtn);

		_skirmishBtn = new Button { Text = "Start skirmish", CustomMinimumSize = new Vector2(150, 36), FocusMode = Control.FocusModeEnum.None };
		_skirmishBtn.Pressed += StartSkirmish;
		actions.AddChild(_skirmishBtn);

		_attackBtn = new Button { Text = "Attack", CustomMinimumSize = new Vector2(100, 36), Disabled = true, FocusMode = Control.FocusModeEnum.None };
		_attackBtn.Pressed += ResolveAttack;
		actions.AddChild(_attackBtn);

		_seatPlayerBtn = new Button { Text = "Seat: Player", CustomMinimumSize = new Vector2(130, 36), FocusMode = Control.FocusModeEnum.None };
		_seatPlayerBtn.Pressed += () => SwitchSeat(SeatId.Player);
		actions.AddChild(_seatPlayerBtn);

		_seatDmBtn = new Button { Text = "Seat: DM", CustomMinimumSize = new Vector2(110, 36), FocusMode = Control.FocusModeEnum.None };
		_seatDmBtn.Pressed += () => SwitchSeat(SeatId.DmAsPlayer);
		actions.AddChild(_seatDmBtn);

		_dmRailBtn = new Button { Text = "DM cam", CustomMinimumSize = new Vector2(130, 36), FocusMode = Control.FocusModeEnum.None };
		_dmRailBtn.Pressed += ToggleDmRail;
		actions.AddChild(_dmRailBtn);

		_backDoorBtn = new Button { Text = "Front door", CustomMinimumSize = new Vector2(120, 36), FocusMode = Control.FocusModeEnum.None };
		_backDoorBtn.Pressed += () =>
		{
			_cams?.ReleaseMouseCapture();
			Input.MouseMode = Input.MouseModeEnum.Visible;
			ReturnToFrontDoor?.Invoke();
		};
		actions.AddChild(_backDoorBtn);

		_controls = new Label
		{
			Text = "WASD move · Mouse look · Esc free mouse (no quit) · click recapture · C skill · V skirmish · B attack · Tab DM cam",
			Position = new Vector2(24, 490),
			MouseFilter = Control.MouseFilterEnum.Ignore,
		};
		_controls.AddThemeFontSizeOverride("font_size", 13);
		_controls.AddThemeColorOverride("font_color", new Color(0.72f, 0.75f, 0.8f));
		_hud.AddChild(_controls);
	}

	private void RefreshHud()
	{
		if (_pack == null || _pc == null || _site == null) return;
		if (_hudTitle != null)
			_hudTitle.Text = $"{_pack.Title} · {_site.Name}";
		if (_hudBody != null)
			_hudBody.Text = $"{_site.Blurb}\nPack id: {_pack.PackId} · rules: {_pack.RulesetBind}";
		if (_hudSheet != null)
			_hudSheet.Text =
				$"{_pc.Name}  HP {_pc.Hp}/{_pc.HpMax}  AC {_pc.Ac}  atk +{_pc.AttackMod}  dmg {_pc.Damage}  ·  {_pc.SkillsSummary()}";
		if (_seatBadge != null)
			_seatBadge.Text = _activeSeat == SeatId.DmAsPlayer
				? "Active seat: DM"
				: "Active seat: Player";
		if (_skillBtn != null) _skillBtn.Disabled = _skillDone;
		if (_skirmishBtn != null) _skirmishBtn.Disabled = !_skillDone || _skirmishStarted;
		if (_attackBtn != null) _attackBtn.Disabled = !_skirmishStarted || _skirmishOver || _activeSeat != SeatId.Player;
	}

	private void SwitchSeat(SeatId seat)
	{
		_activeSeat = seat;
		HideToast();
		if (_agency != null)
		{
			_ = _agency.Release("pilot_default");
			_agency.Assert(new SeatContext(seat));
		}
		RefreshHud();
		ApplySeatCamera(showRefuseToast: false);
		SetResult(seat == SeatId.DmAsPlayer
			? "Switched to DM seat — DM rail allowed."
			: "Switched to Player seat — FP control. DM rail will refuse.");
	}

	private void ApplySeatCamera(bool showRefuseToast)
	{
		if (_cams == null) return;
		if (_activeSeat == SeatId.DmAsPlayer)
		{
			_cams.Activate(PerspectiveMode.DmWorldCam, SeatContext.DmAsPlayer);
		}
		else
		{
			_cams.Activate(PerspectiveMode.FirstPerson, SeatContext.Player);
			_cams.SetFpControl(true);
		}
		if (showRefuseToast)
		{
			var refuse = _cams.Activate(PerspectiveMode.DmWorldCam, SeatContext.Player);
			if (refuse == Error.Unauthorized)
				ShowToast("Unauthorized — player seat cannot own DM table rail");
		}
	}

	private void ToggleDmRail()
	{
		if (_cams == null) return;

		if (_activeSeat == SeatId.Player)
		{
			var refuse = _cams.Activate(PerspectiveMode.DmWorldCam, SeatContext.Player);
			if (refuse == Error.Unauthorized)
				ShowToast("Unauthorized — player seat cannot own DM table rail");
			_cams.Activate(PerspectiveMode.FirstPerson, SeatContext.Player);
			_cams.SetFpControl(true);
			return;
		}

		if (_cams.ActiveMode == PerspectiveMode.DmWorldCam)
		{
			_cams.Activate(PerspectiveMode.FirstPerson, SeatContext.DmAsPlayer);
			_cams.SetFpControl(true);
			SetResult("DM seat — dropped to FP eye over the same site (still DM seat).");
		}
		else
		{
			_cams.Activate(PerspectiveMode.DmWorldCam, SeatContext.DmAsPlayer);
			SetResult("DM aerial / table rail over the same place.");
		}
	}

	private void RunSkillCheck()
	{
		if (_pack == null || _pc == null || _rules == null) return;
		if (_activeSeat != SeatId.Player)
		{
			ShowToast("Unauthorized — skill check is a Player seat action");
			return;
		}

		var beat = _pack.SkillCheck;
		var mod = _pc.SkillModOrDefault(beat.SkillId, 0);
		_rollSeed++;
		var result = _rules.Evaluate(new CheckRequest
		{
			Mode = "check",
			Roll = "1d20",
			Modifier = mod,
			Dc = beat.Dc,
			RulesSubSeed = _rollSeed,
		});
		var d20 = result.Audit?.Rolls.Count > 0 ? (int)result.Audit.Rolls[0].AsInt32() : result.Total - mod;
		var outcome = result.Passed ? "SUCCESS" : "FAILURE";
		SetResult(
			$"{beat.Title}\n" +
			$"d20 ({d20}) + {beat.SkillFallbackLabel} ({mod:+#;-#;0}) = {result.Total} vs DC {beat.Dc} → {outcome}\n" +
			$"(pathfinder_pf1 via rules plugin host)");
		_skillDone = true;
		RefreshHud();
	}

	private void StartSkirmish()
	{
		if (_pack == null || _pc == null || _enemy == null || _rules == null) return;
		if (_activeSeat != SeatId.Player)
		{
			ShowToast("Unauthorized — skirmish start is a Player seat action");
			return;
		}

		_rollSeed++;
		var pcInit = _rules.Roll(DiceExpression.Parse("1d20"), RuleContextFrame.FromRulesSeed(_rollSeed)).Total;
		_rollSeed++;
		var enInitAudit = _rules.Roll(DiceExpression.Parse($"1d20+{_enemy.InitiativeMod}"),
			RuleContextFrame.FromRulesSeed(_rollSeed));
		_playerWinsInit = pcInit >= enInitAudit.Total;
		_skirmishStarted = true;
		_skirmishOver = false;
		SetResult(
			$"{_pack.Skirmish.Title}\n" +
			$"Initiative — {_pc.Name}: d20={pcInit}  |  {_enemy.Name}: {enInitAudit.Total} " +
			$"(d20+{_enemy.InitiativeMod})\n" +
			$"{(_playerWinsInit ? _pc.Name : _enemy.Name)} acts first. Press Attack.");
		RefreshHud();
	}

	private void ResolveAttack()
	{
		if (_pack == null || _pc == null || _enemy == null || _rules == null) return;
		if (_activeSeat != SeatId.Player)
		{
			ShowToast("Unauthorized — attack is a Player seat action");
			return;
		}
		if (!_skirmishStarted || _skirmishOver) return;

		var log = new System.Text.StringBuilder();
		log.AppendLine(_pack.Skirmish.Title);

		if (_playerWinsInit)
		{
			ResolveOneAttack(log, attackerIsPc: true);
			if (_enemy.Hp > 0)
				ResolveOneAttack(log, attackerIsPc: false);
		}
		else
		{
			ResolveOneAttack(log, attackerIsPc: false);
			if (_pc.Hp > 0)
				ResolveOneAttack(log, attackerIsPc: true);
		}

		if (_enemy.Hp <= 0)
		{
			_skirmishOver = true;
			log.AppendLine($"{_enemy.Name} drops — scrap over.");
		}
		else if (_pc.Hp <= 0)
		{
			_pc.Hp = 0;
			_skirmishOver = true;
			log.AppendLine($"{_pc.Name} is down — scrap over (placeholder).");
		}
		else
		{
			log.AppendLine("Press Attack again for another exchange.");
		}

		SetResult(log.ToString().TrimEnd());
		RefreshHud();
	}

	private void ResolveOneAttack(System.Text.StringBuilder log, bool attackerIsPc)
	{
		if (_pc == null || _enemy == null || _rules == null) return;
		_rollSeed++;
		if (attackerIsPc)
		{
			var atk = _rules.Evaluate(new CheckRequest
			{
				Mode = "attack",
				Roll = "1d20",
				Modifier = _pc.AttackMod,
				Dc = _enemy.Ac,
				RulesSubSeed = _rollSeed,
			});
			var d20 = atk.Audit?.Rolls.Count > 0 ? (int)atk.Audit.Rolls[0].AsInt32() : atk.Total - _pc.AttackMod;
			log.AppendLine(
				$"{_pc.Name} attack: d20 ({d20}) + {_pc.AttackMod} = {atk.Total} vs AC {_enemy.Ac} → {(atk.Passed ? "HIT" : "MISS")}");
			if (atk.Passed)
			{
				_rollSeed++;
				var dmg = _rules.Roll(DiceExpression.Parse(_pc.Damage), RuleContextFrame.FromRulesSeed(_rollSeed));
				_enemy.Hp = System.Math.Max(0, _enemy.Hp - dmg.Total);
				log.AppendLine($"  Damage {_pc.Damage} = {dmg.Total} → {_enemy.Name} HP {_enemy.Hp}/{_enemy.HpMax}");
			}
		}
		else
		{
			var atk = _rules.Evaluate(new CheckRequest
			{
				Mode = "attack",
				Roll = "1d20",
				Modifier = _enemy.AttackMod,
				Dc = _pc.Ac,
				RulesSubSeed = _rollSeed,
			});
			var d20 = atk.Audit?.Rolls.Count > 0 ? (int)atk.Audit.Rolls[0].AsInt32() : atk.Total - _enemy.AttackMod;
			log.AppendLine(
				$"{_enemy.Name} attack: d20 ({d20}) + {_enemy.AttackMod} = {atk.Total} vs AC {_pc.Ac} → {(atk.Passed ? "HIT" : "MISS")}");
			if (atk.Passed)
			{
				_rollSeed++;
				var dmg = _rules.Roll(DiceExpression.Parse(_enemy.Damage), RuleContextFrame.FromRulesSeed(_rollSeed));
				_pc.Hp = System.Math.Max(0, _pc.Hp - dmg.Total);
				log.AppendLine($"  Damage {_enemy.Damage} = {dmg.Total} → {_pc.Name} HP {_pc.Hp}/{_pc.HpMax}");
			}
		}
	}

	private void SetResult(string text)
	{
		if (_hudResult != null) _hudResult.Text = text;
	}

	private void ShowToast(string message)
	{
		if (_toast != null)
		{
			_toast.Visible = true;
			_toast.Text = message;
		}
		if (_toastBg != null) _toastBg.Visible = true;
	}

	private void HideToast()
	{
		if (_toast != null) _toast.Visible = false;
		if (_toastBg != null) _toastBg.Visible = false;
	}

	public override void _Input(InputEvent @event)
	{
		if (!Visible) return;

		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.Escape })
		{
			// Esc frees mouse only — MUST NOT quit the project.
			_cams?.ReleaseMouseCapture();
			Input.MouseMode = Input.MouseModeEnum.Visible;
			GetViewport().SetInputAsHandled();
			return;
		}

		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.Tab })
		{
			if (_cams == null) return;
			// Tab → DM cam (offline: takes DM seat). Seat: Player returns FP + recapture.
			if (_activeSeat == SeatId.Player)
				SwitchSeat(SeatId.DmAsPlayer);
			else
				ToggleDmRail();
			GetViewport().SetInputAsHandled();
			return;
		}
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (!Visible) return;

		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.C })
		{
			RunSkillCheck();
			GetViewport().SetInputAsHandled();
			return;
		}
		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.V })
		{
			StartSkirmish();
			GetViewport().SetInputAsHandled();
			return;
		}
		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.B })
		{
			ResolveAttack();
			GetViewport().SetInputAsHandled();
			return;
		}
	}

	private static EnemyDef CloneEnemy(EnemyDef e) => new()
	{
		Id = e.Id,
		Name = e.Name,
		Hp = e.Hp,
		HpMax = e.HpMax,
		AttackMod = e.AttackMod,
		Damage = e.Damage,
		Ac = e.Ac,
		InitiativeMod = e.InitiativeMod,
	};

	private static void PublishRequiredSeams(SeamRegistry seams)
	{
		StringName[] ids =
		{
			"gen.stage.terrain", "gen.stage.biomes", "gen.stage.pois", "gen.stage.entities",
			"gen.stage.sim_bootstrap", "rules.plugin.core", "bus.sub.sim_default",
			"bus.sub.canon_default", "input.parser.player_lite"
		};
		foreach (var id in ids)
		{
			seams.Publish(new SeamEntry
			{
				SeamId = id,
				Family = id.ToString().StartsWith("rules") ? SeamFamily.Rules
					: id.ToString().StartsWith("bus") ? SeamFamily.Bus
					: id.ToString().StartsWith("input") ? SeamFamily.Input
					: SeamFamily.Generation,
				PortOwner = "SessionComposer",
				Lifecycle = SeamLifecycle.Published
			});
		}
	}
}

internal static class PregenRuntimeExt
{
	public static PregenCharacter CloneRuntime(this PregenCharacter p) => new()
	{
		Id = p.Id,
		Name = p.Name,
		AncestryLabel = p.AncestryLabel,
		Hp = p.Hp,
		HpMax = p.HpMax,
		AttackMod = p.AttackMod,
		Damage = p.Damage,
		Ac = p.Ac,
		Skills = new System.Collections.Generic.List<SkillMod>(p.Skills),
	};
}
