using System.Collections.Generic;
using Godot;
using Godot.Collections;

namespace Genesis.Module;

/// <summary>
/// Loads module cartridges from res://content/packs/&lt;pack_id&gt;/.
/// Pack boundary = JSON on disk with stable pack_id — not hardcoded-only scenes.
/// </summary>
public static class ModulePackLoader
{
	public const string PacksRoot = "res://content/packs";
	public const string ExampleGoblinPackId = "example_goblin_oneshot"; // shape feedstock only
	public const string DefaultCartridgePackId = "we_be_goblins_free_struct";

	public static List<ModulePackCatalogEntry> ListAvailablePacks()
	{
		var list = new List<ModulePackCatalogEntry>();
		using var dir = DirAccess.Open(PacksRoot);
		if (dir == null) return list;

		dir.ListDirBegin();
		while (true)
		{
			var name = dir.GetNext();
			if (string.IsNullOrEmpty(name)) break;
			if (!dir.CurrentIsDir() || name.StartsWith('.')) continue;
			var root = $"{PacksRoot}/{name}";
			var packPath = $"{root}/pack.json";
			if (!Godot.FileAccess.FileExists(packPath)) continue;
			var raw = Godot.FileAccess.GetFileAsString(packPath);
			var parsed = Json.ParseString(raw);
			if (parsed.VariantType != Variant.Type.Dictionary) continue;
			var d = parsed.AsGodotDictionary();
			list.Add(new ModulePackCatalogEntry
			{
				PackId = DictStr(d, "pack_id", name),
				Title = DictStr(d, "title", name),
				Subtitle = DictStr(d, "subtitle", ""),
				PackRootResPath = root,
			});
		}
		dir.ListDirEnd();

		// Stable Alpha 0 expectation: example pack always listed if present.
		list.Sort((a, b) => string.CompareOrdinal(a.PackId, b.PackId));
		return list;
	}

	public static Error Load(string packId, out ModulePack? pack, out string error)
	{
		pack = null;
		error = "";
		if (string.IsNullOrWhiteSpace(packId))
		{
			error = "empty pack_id";
			return Error.InvalidParameter;
		}

		var root = $"{PacksRoot}/{packId}";
		var packPath = $"{root}/pack.json";
		if (!Godot.FileAccess.FileExists(packPath))
		{
			error = $"missing {packPath}";
			return Error.DoesNotExist;
		}

		var packDict = ReadDict(packPath, out error);
		if (packDict == null) return Error.ParseError;

		var loadedId = DictStr(packDict, "pack_id", packId);
		if (loadedId != packId)
		{
			error = $"pack_id mismatch file={loadedId} requested={packId}";
			return Error.InvalidData;
		}

		var pregensFile = DictStr(packDict, "pregens_file", "pregens.json");
		var sitesFile = DictStr(packDict, "sites_file", "sites.json");
		var beatsFile = DictStr(packDict, "beats_file", "beats.json");

		var pregensDict = ReadDict($"{root}/{pregensFile}", out error);
		if (pregensDict == null) return Error.ParseError;
		var sitesDict = ReadDict($"{root}/{sitesFile}", out error);
		if (sitesDict == null) return Error.ParseError;
		var beatsDict = ReadDict($"{root}/{beatsFile}", out error);
		if (beatsDict == null) return Error.ParseError;

		var pregens = ParsePregens(pregensDict);
		var sites = ParseSites(sitesDict);
		if (pregens.Count < 2)
		{
			error = "pack requires ≥2 pregens";
			return Error.InvalidData;
		}
		if (sites.Count < 1)
		{
			error = "pack requires ≥1 site";
			return Error.InvalidData;
		}

		var skill = ParseSkillCheck(beatsDict);
		var skirmish = ParseSkirmish(beatsDict);
		if (skill == null || skirmish == null)
		{
			error = "pack requires skill_check and skirmish beats";
			return Error.InvalidData;
		}

		var stages = ParseStages(beatsDict);
		if (stages.Count == 0)
		{
			// Backward-compatible single stage from legacy skill_check + skirmish.
			stages.Add(new AdventureStage
			{
				Id = "legacy_default",
				SiteId = DictStr(packDict, "default_site_id", sites[0].Id),
				Title = skill.Title,
				ExploreBlurb = skill.Blurb,
				RequireIntentBeforeAdvance = false,
				Intents =
				{
					new IntentBeat
					{
						Id = skill.Id,
						Kind = "skill",
						Verb = "Check",
						Title = skill.Title,
						SkillId = skill.SkillId,
						SkillFallbackLabel = skill.SkillFallbackLabel,
						Dc = skill.Dc,
						Blurb = skill.Blurb,
					},
					new IntentBeat
					{
						Id = skirmish.Id,
						Kind = "skirmish",
						Verb = "Fight",
						Title = skirmish.Title,
						Blurb = skirmish.Blurb,
						Enemy = skirmish.Enemy,
					},
				},
			});
		}

		pack = new ModulePack
		{
			PackId = loadedId,
			Title = DictStr(packDict, "title", loadedId),
			Subtitle = DictStr(packDict, "subtitle", ""),
			RulesetBind = DictStr(packDict, "ruleset_bind", "pathfinder_pf1"),
			ReleaseStage = DictStr(packDict, "release_stage", "alpha_0"),
			Honesty = DictStr(packDict, "honesty", ""),
			DefaultSiteId = DictStr(packDict, "default_site_id", sites[0].Id),
			PackRootResPath = root,
			Pregens = pregens,
			Sites = sites,
			SkillCheck = skill,
			Skirmish = skirmish,
			Stages = stages,
			Relationships = ParseRelationships(beatsDict),
		};
		error = "";
		return Error.Ok;
	}


	private static List<AdventureStage> ParseStages(Dictionary beats)
	{
		var list = new List<AdventureStage>();
		if (!beats.ContainsKey("stages") || beats["stages"].VariantType != Variant.Type.Array)
			return list;
		foreach (var item in beats["stages"].AsGodotArray())
		{
			if (item.VariantType != Variant.Type.Dictionary) continue;
			var d = item.AsGodotDictionary();
			var intents = new List<IntentBeat>();
			if (d.ContainsKey("intents") && d["intents"].VariantType == Variant.Type.Array)
			{
				foreach (var rawIntent in d["intents"].AsGodotArray())
				{
					if (rawIntent.VariantType != Variant.Type.Dictionary) continue;
					var id = rawIntent.AsGodotDictionary();
					EnemyDef? enemy = null;
					if (id.ContainsKey("enemy") && id["enemy"].VariantType == Variant.Type.Dictionary)
					{
						var e = id["enemy"].AsGodotDictionary();
						enemy = new EnemyDef
						{
							Id = DictStr(e, "id", "enemy"),
							Name = DictStr(e, "name", "Enemy"),
							Hp = DictInt(e, "hp", 6),
							HpMax = DictInt(e, "hp_max", DictInt(e, "hp", 6)),
							AttackMod = DictInt(e, "attack_mod", 0),
							Damage = DictStr(e, "damage", "1d4"),
							Ac = DictInt(e, "ac", 10),
							InitiativeMod = DictInt(e, "initiative_mod", 0),
						};
					}
					intents.Add(new IntentBeat
					{
						Id = DictStr(id, "id", $"intent_{intents.Count}"),
						Kind = DictStr(id, "kind", "skill"),
						Verb = DictStr(id, "verb", "Act"),
						Title = DictStr(id, "title", "Intent"),
						SkillId = DictStr(id, "skill_id", "perception"),
						SkillFallbackLabel = DictStr(id, "skill_fallback_label", "Skill"),
						Dc = DictInt(id, "dc", 10),
						Blurb = DictStr(id, "blurb", ""),
						Enemy = enemy,
					});
				}
			}
			list.Add(new AdventureStage
			{
				Id = DictStr(d, "id", $"stage_{list.Count}"),
				SiteId = DictStr(d, "site_id", ""),
				Title = DictStr(d, "title", "Stage"),
				ExploreBlurb = DictStr(d, "explore_blurb", ""),
				RequireIntentBeforeAdvance = !d.ContainsKey("require_intent_before_advance")
					|| d["require_intent_before_advance"].AsBool(),
				Intents = intents,
			});
		}
		return list;
	}

	private static List<RelationshipEntry> ParseRelationships(Dictionary beats)
	{
		var list = new List<RelationshipEntry>();
		if (!beats.ContainsKey("relationships") || beats["relationships"].VariantType != Variant.Type.Array)
			return list;
		foreach (var item in beats["relationships"].AsGodotArray())
		{
			if (item.VariantType != Variant.Type.Dictionary) continue;
			var d = item.AsGodotDictionary();
			var hooks = new List<string>();
			if (d.ContainsKey("rp_hooks") && d["rp_hooks"].VariantType == Variant.Type.Array)
			{
				foreach (var h in d["rp_hooks"].AsGodotArray())
					hooks.Add(h.AsString());
			}
			list.Add(new RelationshipEntry
			{
				NpcId = DictStr(d, "npc_id", ""),
				Label = DictStr(d, "label", ""),
				Disposition = DictStr(d, "disposition", ""),
				History = DictStr(d, "history", ""),
				RpHooks = hooks,
			});
		}
		return list;
	}

	private static Dictionary? ReadDict(string path, out string error)
	{
		error = "";
		if (!Godot.FileAccess.FileExists(path))
		{
			error = $"missing {path}";
			return null;
		}
		var raw = Godot.FileAccess.GetFileAsString(path);
		var parsed = Json.ParseString(raw);
		if (parsed.VariantType != Variant.Type.Dictionary)
		{
			error = $"not a JSON object: {path}";
			return null;
		}
		return parsed.AsGodotDictionary();
	}

	private static List<PregenCharacter> ParsePregens(Dictionary root)
	{
		var list = new List<PregenCharacter>();
		if (!root.ContainsKey("pregens") || root["pregens"].VariantType != Variant.Type.Array)
			return list;
		foreach (var item in root["pregens"].AsGodotArray())
		{
			if (item.VariantType != Variant.Type.Dictionary) continue;
			var d = item.AsGodotDictionary();
			var skills = new List<SkillMod>();
			if (d.ContainsKey("skills") && d["skills"].VariantType == Variant.Type.Array)
			{
				foreach (var sk in d["skills"].AsGodotArray())
				{
					if (sk.VariantType != Variant.Type.Dictionary) continue;
					var sd = sk.AsGodotDictionary();
					skills.Add(new SkillMod
					{
						Id = DictStr(sd, "id", ""),
						Label = DictStr(sd, "label", DictStr(sd, "id", "skill")),
						Mod = DictInt(sd, "mod", 0),
					});
				}
			}
			list.Add(new PregenCharacter
			{
				Id = DictStr(d, "id", ""),
				Name = DictStr(d, "name", "Unnamed"),
				AncestryLabel = DictStr(d, "ancestry_label", ""),
				Hp = DictInt(d, "hp", 8),
				HpMax = DictInt(d, "hp_max", DictInt(d, "hp", 8)),
				AttackMod = DictInt(d, "attack_mod", 0),
				Damage = DictStr(d, "damage", "1d4"),
				Ac = DictInt(d, "ac", 10),
				Skills = skills,
			});
		}
		return list;
	}

	private static List<SiteDef> ParseSites(Dictionary root)
	{
		var list = new List<SiteDef>();
		if (!root.ContainsKey("sites") || root["sites"].VariantType != Variant.Type.Array)
			return list;
		foreach (var item in root["sites"].AsGodotArray())
		{
			if (item.VariantType != Variant.Type.Dictionary) continue;
			var d = item.AsGodotDictionary();
			list.Add(new SiteDef
			{
				Id = DictStr(d, "id", ""),
				Name = DictStr(d, "name", "Site"),
				Kind = DictStr(d, "kind", "path"),
				Blurb = DictStr(d, "blurb", ""),
				SpawnEye = DictVec3(d, "spawn_eye", new Vector3(0f, 1.65f, 7.5f)),
				DmEye = DictVec3(d, "dm_eye", new Vector3(0f, 16f, 10f)),
				Theme = DictStr(d, "theme", ""),
			});
		}
		return list;
	}

	private static SkillCheckBeat? ParseSkillCheck(Dictionary beats)
	{
		if (!beats.ContainsKey("skill_check") || beats["skill_check"].VariantType != Variant.Type.Dictionary)
			return null;
		var d = beats["skill_check"].AsGodotDictionary();
		return new SkillCheckBeat
		{
			Id = DictStr(d, "id", "skill_check"),
			Title = DictStr(d, "title", "Skill check"),
			SkillId = DictStr(d, "skill_id", "stealth"),
			SkillFallbackLabel = DictStr(d, "skill_fallback_label", "Skill"),
			Dc = DictInt(d, "dc", 10),
			Blurb = DictStr(d, "blurb", ""),
		};
	}

	private static SkirmishBeat? ParseSkirmish(Dictionary beats)
	{
		if (!beats.ContainsKey("skirmish") || beats["skirmish"].VariantType != Variant.Type.Dictionary)
			return null;
		var d = beats["skirmish"].AsGodotDictionary();
		EnemyDef enemy = new();
		if (d.ContainsKey("enemy") && d["enemy"].VariantType == Variant.Type.Dictionary)
		{
			var e = d["enemy"].AsGodotDictionary();
			enemy = new EnemyDef
			{
				Id = DictStr(e, "id", "enemy"),
				Name = DictStr(e, "name", "Enemy"),
				Hp = DictInt(e, "hp", 6),
				HpMax = DictInt(e, "hp_max", DictInt(e, "hp", 6)),
				AttackMod = DictInt(e, "attack_mod", 0),
				Damage = DictStr(e, "damage", "1d4"),
				Ac = DictInt(e, "ac", 10),
				InitiativeMod = DictInt(e, "initiative_mod", 0),
			};
		}
		return new SkirmishBeat
		{
			Id = DictStr(d, "id", "skirmish"),
			Title = DictStr(d, "title", "Skirmish"),
			Blurb = DictStr(d, "blurb", ""),
			Enemy = enemy,
		};
	}

	private static string DictStr(Dictionary d, string key, string fallback) =>
		d.ContainsKey(key) ? d[key].AsString() : fallback;

	private static int DictInt(Dictionary d, string key, int fallback)
	{
		if (!d.ContainsKey(key)) return fallback;
		return d[key].VariantType switch
		{
			Variant.Type.Int => (int)d[key].AsInt64(),
			Variant.Type.Float => (int)d[key].AsDouble(),
			_ => fallback,
		};
	}

	private static Vector3 DictVec3(Dictionary d, string key, Vector3 fallback)
	{
		if (!d.ContainsKey(key) || d[key].VariantType != Variant.Type.Array) return fallback;
		var a = d[key].AsGodotArray();
		if (a.Count < 3) return fallback;
		return new Vector3((float)a[0].AsDouble(), (float)a[1].AsDouble(), (float)a[2].AsDouble());
	}
}
