using System.Collections.Generic;
using Godot;

namespace Genesis.Module;

public sealed class ModulePackCatalogEntry
{
	public string PackId { get; init; } = "";
	public string Title { get; init; } = "";
	public string Subtitle { get; init; } = "";
	public string PackRootResPath { get; init; } = "";
}

public sealed class SkillMod
{
	public string Id { get; init; } = "";
	public string Label { get; init; } = "";
	public int Mod { get; init; }
}

public sealed class PregenCharacter
{
	public string Id { get; init; } = "";
	public string Name { get; init; } = "";
	public string AncestryLabel { get; init; } = "";
	public int Hp { get; set; }
	public int HpMax { get; init; }
	public int AttackMod { get; init; }
	public string Damage { get; init; } = "1d4";
	public int Ac { get; init; } = 10;
	public List<SkillMod> Skills { get; init; } = new();

	public int SkillModOrDefault(string skillId, int fallback = 0)
	{
		foreach (var s in Skills)
		{
			if (s.Id == skillId) return s.Mod;
		}
		return fallback;
	}

	public string SkillsSummary()
	{
		var parts = new List<string>();
		foreach (var s in Skills)
			parts.Add($"{s.Label} {s.Mod:+#;-#;0}");
		return string.Join(" · ", parts);
	}
}

public sealed class SiteDef
{
	public string Id { get; init; } = "";
	public string Name { get; init; } = "";
	public string Kind { get; init; } = "path";
	public string Blurb { get; init; } = "";
	public Vector3 SpawnEye { get; init; }
	public Vector3 DmEye { get; init; }
	public string Theme { get; init; } = "";
}

public sealed class SkillCheckBeat
{
	public string Id { get; init; } = "";
	public string Title { get; init; } = "";
	public string SkillId { get; init; } = "stealth";
	public string SkillFallbackLabel { get; init; } = "Stealth";
	public int Dc { get; init; } = 10;
	public string Blurb { get; init; } = "";
}

public sealed class EnemyDef
{
	public string Id { get; init; } = "";
	public string Name { get; init; } = "";
	public int Hp { get; set; }
	public int HpMax { get; init; }
	public int AttackMod { get; init; }
	public string Damage { get; init; } = "1d4";
	public int Ac { get; init; } = 10;
	public int InitiativeMod { get; init; }
}

public sealed class SkirmishBeat
{
	public string Id { get; init; } = "";
	public string Title { get; init; } = "";
	public string Blurb { get; init; } = "";
	public EnemyDef Enemy { get; init; } = new();
}

public sealed class ModulePack
{
	public string PackId { get; init; } = "";
	public string Title { get; init; } = "";
	public string Subtitle { get; init; } = "";
	public string RulesetBind { get; init; } = "pathfinder_pf1";
	public string ReleaseStage { get; init; } = "alpha_0";
	public string Honesty { get; init; } = "";
	public string DefaultSiteId { get; init; } = "";
	public string PackRootResPath { get; init; } = "";
	public List<PregenCharacter> Pregens { get; init; } = new();
	public List<SiteDef> Sites { get; init; } = new();
	public SkillCheckBeat SkillCheck { get; init; } = new();
	public SkirmishBeat Skirmish { get; init; } = new();

	public SiteDef? FindSite(string siteId)
	{
		foreach (var s in Sites)
		{
			if (s.Id == siteId) return s;
		}
		return Sites.Count > 0 ? Sites[0] : null;
	}

	public PregenCharacter? FindPregen(string pregenId)
	{
		foreach (var p in Pregens)
		{
			if (p.Id == pregenId) return p;
		}
		return Pregens.Count > 0 ? Pregens[0] : null;
	}
}
