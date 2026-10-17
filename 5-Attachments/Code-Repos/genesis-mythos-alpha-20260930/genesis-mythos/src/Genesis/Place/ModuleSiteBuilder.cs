using Genesis.Module;
using Godot;

namespace Genesis.Place;

/// <summary>Builds a readable site from pack data — path, landmark, alcove. Placeholder art only.</summary>
public static class ModuleSiteBuilder
{
	public static Node3D Build(Node3D parent, SiteDef site)
	{
		var root = new Node3D { Name = $"Site_{site.Id}" };
		parent.AddChild(root);

		var palette = ThemePalette(site.Theme);

		var env = new Godot.Environment
		{
			BackgroundMode = Godot.Environment.BGMode.Color,
			BackgroundColor = palette.Sky,
			AmbientLightSource = Godot.Environment.AmbientSource.Color,
			AmbientLightColor = palette.Ambient,
			TonemapMode = Godot.Environment.ToneMapper.Filmic,
		};
		root.AddChild(new WorldEnvironment { Environment = env });

		var sun = new DirectionalLight3D
		{
			Name = "Sun",
			RotationDegrees = new Vector3(-42f, 28f, 0f),
			LightEnergy = palette.SunEnergy,
			ShadowEnabled = false,
		};
		root.AddChild(sun);

		AddBox(root, "Floor", new Vector3(0f, -0.15f, -2f), new Vector3(22f, 0.3f, 28f), palette.Floor);
		AddBox(root, "Path", new Vector3(0f, 0.02f, 1f), new Vector3(2.4f, 0.08f, 16f), palette.Path);

		AddBox(root, "WallWest", new Vector3(-7f, 1.0f, -1f), new Vector3(0.45f, 2.0f, 20f), palette.Wall);
		AddBox(root, "WallEast", new Vector3(7f, 1.0f, -1f), new Vector3(0.45f, 2.0f, 20f), palette.Wall);
		AddBox(root, "WallNorth", new Vector3(0f, 1.0f, -11f), new Vector3(14.5f, 2.0f, 0.45f), palette.Wall);

		AddBox(root, "CaveLip", new Vector3(0f, 1.6f, 10.2f), new Vector3(5.5f, 3.2f, 1.2f), palette.Landmark);
		AddBox(root, "CaveMouth", new Vector3(0f, 1.2f, 9.4f), new Vector3(2.8f, 2.4f, 0.8f),
			new Color(0.08f, 0.07f, 0.06f));

		AddPillar(root, "LanternL1", new Vector3(-1.6f, 0.7f, 5f), palette.Accent);
		AddPillar(root, "LanternR1", new Vector3(1.6f, 0.7f, 5f), palette.Accent);
		AddPillar(root, "LanternL2", new Vector3(-1.6f, 0.7f, 0f), palette.Accent);
		AddPillar(root, "LanternR2", new Vector3(1.6f, 0.7f, 0f), palette.Accent);

		var clearing = new Node3D { Name = "ScrapClearing", Position = new Vector3(0f, 0f, -7f) };
		root.AddChild(clearing);
		AddBox(clearing, "DirtRing", new Vector3(0f, 0.03f, 0f), new Vector3(5.5f, 0.06f, 5.5f), palette.Clearing);
		AddBox(clearing, "Stump", new Vector3(-1.4f, 0.4f, -1.2f), new Vector3(0.9f, 0.8f, 0.9f),
			new Color(0.45f, 0.34f, 0.22f));
		AddBox(clearing, "EnemyPad", new Vector3(1.2f, 0.05f, 0.8f), new Vector3(1.2f, 0.08f, 1.2f),
			new Color(0.55f, 0.28f, 0.22f));

		if (site.Theme == "campsite_dusk")
		{
			AddBox(root, "Wagon", new Vector3(3.5f, 0.7f, -5f), new Vector3(2.2f, 1.2f, 1.4f),
				new Color(0.42f, 0.28f, 0.18f));
			AddBox(root, "Wagon2", new Vector3(-3.2f, 0.55f, -4.2f), new Vector3(1.8f, 0.9f, 1.2f),
				new Color(0.38f, 0.26f, 0.16f));
		}
		else if (site.Theme == "clearing")
		{
			AddPillar(root, "TruffleMoundA", new Vector3(-2.2f, 0.25f, -6f), new Color(0.35f, 0.42f, 0.22f));
			AddPillar(root, "TruffleMoundB", new Vector3(2.0f, 0.22f, -5.4f), new Color(0.32f, 0.4f, 0.2f));
			AddPillar(root, "TruffleMoundC", new Vector3(0.4f, 0.2f, -8f), new Color(0.3f, 0.38f, 0.18f));
		}

		AddBox(root, "BenchW", new Vector3(-4.5f, 0.35f, -3f), new Vector3(1.8f, 0.4f, 0.55f),
			new Color(0.4f, 0.32f, 0.26f));
		AddBox(root, "BenchE", new Vector3(4.5f, 0.35f, -3f), new Vector3(1.8f, 0.4f, 0.55f),
			new Color(0.4f, 0.32f, 0.26f));

		AddBox(root, "SpawnPad", new Vector3(site.SpawnEye.X, 0.04f, site.SpawnEye.Z),
			new Vector3(1.6f, 0.06f, 1.6f), new Color(0.35f, 0.45f, 0.55f));

		var label = new Label3D
		{
			Name = "SiteLabel",
			Text = $"{site.Name}\n({site.Kind} · {site.Theme})",
			Position = new Vector3(0f, 3.4f, -7f),
			FontSize = 48,
			Modulate = new Color(0.92f, 0.86f, 0.7f),
			Billboard = BaseMaterial3D.BillboardModeEnum.Enabled,
		};
		root.AddChild(label);

		return root;
	}

	private readonly struct SitePalette
	{
		public Color Sky { get; init; }
		public Color Ambient { get; init; }
		public float SunEnergy { get; init; }
		public Color Floor { get; init; }
		public Color Path { get; init; }
		public Color Wall { get; init; }
		public Color Landmark { get; init; }
		public Color Accent { get; init; }
		public Color Clearing { get; init; }
	}

	private static SitePalette ThemePalette(string theme) => theme switch
	{
		"campsite_dusk" => new SitePalette
		{
			Sky = new Color(0.22f, 0.14f, 0.18f),
			Ambient = new Color(0.48f, 0.32f, 0.28f),
			SunEnergy = 0.85f,
			Floor = new Color(0.28f, 0.22f, 0.18f),
			Path = new Color(0.42f, 0.34f, 0.26f),
			Wall = new Color(0.30f, 0.24f, 0.22f),
			Landmark = new Color(0.32f, 0.22f, 0.18f),
			Accent = new Color(0.85f, 0.45f, 0.2f),
			Clearing = new Color(0.4f, 0.3f, 0.22f),
		},
		"clearing" => new SitePalette
		{
			Sky = new Color(0.28f, 0.38f, 0.32f),
			Ambient = new Color(0.4f, 0.55f, 0.42f),
			SunEnergy = 1.25f,
			Floor = new Color(0.22f, 0.32f, 0.2f),
			Path = new Color(0.36f, 0.4f, 0.28f),
			Wall = new Color(0.26f, 0.34f, 0.26f),
			Landmark = new Color(0.3f, 0.36f, 0.24f),
			Accent = new Color(0.55f, 0.7f, 0.35f),
			Clearing = new Color(0.32f, 0.4f, 0.24f),
		},
		_ => new SitePalette // cave_feast default
		{
			Sky = new Color(0.16f, 0.20f, 0.28f),
			Ambient = new Color(0.42f, 0.46f, 0.52f),
			SunEnergy = 1.1f,
			Floor = new Color(0.24f, 0.28f, 0.26f),
			Path = new Color(0.40f, 0.36f, 0.30f),
			Wall = new Color(0.32f, 0.31f, 0.34f),
			Landmark = new Color(0.28f, 0.26f, 0.24f),
			Accent = new Color(0.75f, 0.55f, 0.25f),
			Clearing = new Color(0.38f, 0.32f, 0.24f),
		},
	};

	private static void AddBox(Node3D parent, string name, Vector3 pos, Vector3 size, Color color)
	{
		var body = new StaticBody3D { Name = name, Position = pos };
		var mesh = new MeshInstance3D { Name = "Mesh" };
		mesh.Mesh = new BoxMesh { Size = size };
		mesh.MaterialOverride = new StandardMaterial3D
		{
			AlbedoColor = color,
			Roughness = 0.85f,
		};
		body.AddChild(mesh);
		var col = new CollisionShape3D
		{
			Name = "Collision",
			Shape = new BoxShape3D { Size = size },
		};
		body.AddChild(col);
		parent.AddChild(body);
	}

	private static void AddPillar(Node3D parent, string name, Vector3 pos, Color color)
	{
		AddBox(parent, name, pos, new Vector3(0.35f, 1.4f, 0.35f), color);
	}
}
