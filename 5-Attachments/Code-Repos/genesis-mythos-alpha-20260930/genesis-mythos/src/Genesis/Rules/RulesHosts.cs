using Genesis.Core;
using Genesis.Exemplar;
using Genesis.Seams;
using Godot;
using Godot.Collections;

namespace Genesis.Rules;

public readonly record struct DiceExpression(string Text)
{
	public static DiceExpression Parse(string text) =>
		string.IsNullOrWhiteSpace(text)
			? throw new System.ArgumentException("empty")
			: new(text.Trim());
}

public sealed class RuleContextFrame
{
	public ulong RulesSubSeed { get; init; }
	public static RuleContextFrame FromRulesSeed(ulong seed) => new() { RulesSubSeed = seed };
}

public sealed class DiceAudit
{
	public string Expression { get; init; } = "";
	public int Total { get; init; }
	public ulong SeedChannel { get; init; }
	public Godot.Collections.Array Rolls { get; init; } = new();
}

public sealed class CheckRequest
{
	public StringName Mode { get; init; } = "check";
	public string Roll { get; init; } = "1d20";
	public int Modifier { get; init; }
	public int Dc { get; init; } = 10;
	/// <summary>Optional seed channel for PF1-shaped rolls (Alpha 0 table).</summary>
	public ulong RulesSubSeed { get; init; } = 42UL;
}
public sealed class CheckResult
{
	public bool Passed { get; init; }
	public int Total { get; init; }
	public StringName Outcome { get; init; } = default;
	public DiceAudit? Audit { get; init; }
}

public interface IDiceRoller
{
	DiceAudit Roll(DiceExpression expression, RuleContextFrame frame);
	DiceAudit RollExpression(string expression, ulong rulesSubSeed);
}

public interface IRulesetPlugin
{
	StringName PluginId { get; }
	CheckResult Evaluate(CheckRequest req, IDiceRoller dice);
}

public interface IRulesPluginHost
{
	Error BindPlugin(IRulesetPlugin plugin);
	CheckResult Evaluate(CheckRequest req);
	DiceAudit Roll(DiceExpression expression, RuleContextFrame frame);
	StringName ActiveRuleset { get; }
}

/// <summary>Deterministic placeholder dice (no AGPL). Seeded from rules channel.</summary>
public sealed class SeededDiceRoller : IDiceRoller
{
	public DiceAudit Roll(DiceExpression expression, RuleContextFrame frame)
	{
		if (string.IsNullOrWhiteSpace(expression.Text))
			throw new System.ArgumentException("empty expression");
		var rng = new System.Random(unchecked((int)frame.RulesSubSeed));
		var total = ParseAndRoll(expression.Text, rng, out var rolls);
		return new DiceAudit
		{
			Expression = expression.Text,
			Total = total,
			SeedChannel = frame.RulesSubSeed,
			Rolls = rolls
		};
	}

	public DiceAudit RollExpression(string expression, ulong rulesSubSeed)
	{
		if (string.IsNullOrWhiteSpace(expression))
			throw new System.ArgumentException("empty expression");
		return Roll(DiceExpression.Parse(expression), RuleContextFrame.FromRulesSeed(rulesSubSeed));
	}

	private static int ParseAndRoll(string expr, System.Random rng, out Godot.Collections.Array rolls)
	{
		rolls = new Godot.Collections.Array();
		// Minimal: NdM+K / NdM / plain int. Enough for PF1 demo probe.
		var text = expr.Replace(" ", "");
		var mod = 0;
		var plus = text.LastIndexOf('+');
		var minus = text.LastIndexOf('-');
		var splitAt = plus > 0 ? plus : (minus > 0 ? minus : -1);
		string dicePart = text;
		if (splitAt > 0)
		{
			dicePart = text[..splitAt];
			mod = int.Parse(text[splitAt..]);
		}
		if (!dicePart.Contains('d') && !dicePart.Contains('D'))
			return int.Parse(dicePart) + mod;
		var parts = dicePart.ToLowerInvariant().Split('d');
		var n = int.Parse(parts[0]);
		var m = int.Parse(parts[1]);
		var sum = 0;
		for (var i = 0; i < n; i++)
		{
			var r = rng.Next(1, m + 1);
			rolls.Add(r);
			sum += r;
		}
		return sum + mod;
	}
}

public sealed class PathfinderPf1Plugin : IRulesetPlugin
{
	public StringName PluginId => "pathfinder_pf1";

	public CheckResult Evaluate(CheckRequest req, IDiceRoller dice)
	{
		var expr = req.Modifier >= 0 ? $"{req.Roll}+{req.Modifier}" : $"{req.Roll}{req.Modifier}";
		var audit = dice.RollExpression(expr, req.RulesSubSeed == 0 ? 42UL : req.RulesSubSeed);
		var passed = audit.Total >= req.Dc;
		var outcome = req.Mode.ToString() == "attack"
			? (passed ? "attack_hit" : "attack_miss")
			: (passed ? "check_pass" : "check_fail");
		return new CheckResult
		{
			Passed = passed,
			Total = audit.Total,
			Outcome = outcome,
			Audit = audit
		};
	}
}

public sealed class RulesPluginHost : IRulesPluginHost
{
	private readonly IDiceRoller _dice;
	private readonly ISeamRegistry _seams;
	private IRulesetPlugin? _plugin;
	private ReceiptLedger? _ledger;

	public RulesPluginHost(IDiceRoller dice, ISeamRegistry seams)
	{
		_dice = dice;
		_seams = seams;
	}

	public StringName ActiveRuleset => _plugin?.PluginId ?? default;

	public void BindLedger(ReceiptLedger ledger) => _ledger = ledger;

	public Error BindPlugin(IRulesetPlugin plugin)
	{
		if (plugin == null) return Error.InvalidParameter;
		var seam = _seams.AssertPublished("rules.plugin.core");
		if (seam != Error.Ok) return Error.Unavailable;
		_plugin = plugin;
		_ledger?.Record("R.rules.pf1_bind", "placeholder_ok",
			"ActiveRuleset=pathfinder_pf1;RollDelegate=IDiceRoller",
			"rules.plugin_id", "slot.rules.plugin");
		return Error.Ok;
	}

	public CheckResult Evaluate(CheckRequest req)
	{
		if (_plugin == null)
			return new CheckResult { Passed = false, Outcome = "unconfigured" };
		return _plugin.Evaluate(req, _dice);
	}

	public DiceAudit Roll(DiceExpression expression, RuleContextFrame frame) =>
		_dice.Roll(expression, frame);
}
