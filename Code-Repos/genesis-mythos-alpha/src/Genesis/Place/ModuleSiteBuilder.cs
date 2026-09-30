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

		var env = new Godot.Environment
		{
			BackgroundMode = Godot.Environment.BGMode.Color,
			BackgroundColor = new Color(0.16f, 0.20f, 0.28f),
			AmbientLightSource = Godot.Environment.AmbientSource.Color,
			AmbientLightColor = new Color(0.42f, 0.46f, 0.52f),
			TonemapMode = Godot.Environment.ToneMapper.Filmic,
		};
		root.AddChild(new WorldEnvironment { Environment = env });

		var sun = new DirectionalLight3D
		{
			Name = "Sun",
			RotationDegrees = new Vector3(-42f, 28f, 0f),
			LightEnergy = 1.1f,
			ShadowEnabled = false,
		};
		root.AddChild(sun);

		AddBox(root, "Floor", new Vector3(0f, -0.15f, -2f), new Vector3(22f, 0.3f, 28f),
			new Color(0.24f, 0.28f, 0.26f));
		AddBox(root, "Path", new Vector3(0f, 0.02f, 1f), new Vector3(2.4f, 0.08f, 16f),
			new Color(0.40f, 0.36f, 0.30f));

		AddBox(root, "WallWest", new Vector3(-7f, 1.0f, -1f), new Vector3(0.45f, 2.0f, 20f),
			new Color(0.32f, 0.31f, 0.34f));
		AddBox(root, "WallEast", new Vector3(7f, 1.0f, -1f), new Vector3(0.45f, 2.0f, 20f),
			new Color(0.32f, 0.31f, 0.34f));
		AddBox(root, "WallNorth", new Vector3(0f, 1.0f, -11f), new Vector3(14.5f, 2.0f, 0.45f),
			new Color(0.30f, 0.29f, 0.32f));

		// Cave mouth landmark (south back)
		AddBox(root, "CaveLip", new Vector3(0f, 1.6f, 10.2f), new Vector3(5.5f, 3.2f, 1.2f),
			new Color(0.28f, 0.26f, 0.24f));
		AddBox(root, "CaveMouth", new Vector3(0f, 1.2f, 9.4f), new Vector3(2.8f, 2.4f, 0.8f),
			new Color(0.08f, 0.07f, 0.06f));

		AddPillar(root, "LanternL1", new Vector3(-1.6f, 0.7f, 5f), new Color(0.75f, 0.55f, 0.25f));
		AddPillar(root, "LanternR1", new Vector3(1.6f, 0.7f, 5f), new Color(0.75f, 0.55f, 0.25f));
		AddPillar(root, "LanternL2", new Vector3(-1.6f, 0.7f, 0f), new Color(0.7f, 0.5f, 0.22f));
		AddPillar(root, "LanternR2", new Vector3(1.6f, 0.7f, 0f), new Color(0.7f, 0.5f, 0.22f));

		// Scrap clearing landmark (north)
		var clearing = new Node3D { Name = "ScrapClearing", Position = new Vector3(0f, 0f, -7f) };
		root.AddChild(clearing);
		AddBox(clearing, "DirtRing", new Vector3(0f, 0.03f, 0f), new Vector3(5.5f, 0.06f, 5.5f),
			new Color(0.38f, 0.32f, 0.24f));
		AddBox(clearing, "Stump", new Vector3(-1.4f, 0.4f, -1.2f), new Vector3(0.9f, 0.8f, 0.9f),
			new Color(0.45f, 0.34f, 0.22f));
		AddBox(clearing, "EnemyPad", new Vector3(1.2f, 0.05f, 0.8f), new Vector3(1.2f, 0.08f, 1.2f),
			new Color(0.55f, 0.28f, 0.22f));

		AddBox(root, "BenchW", new Vector3(-4.5f, 0.35f, -3f), new Vector3(1.8f, 0.4f, 0.55f),
			new Color(0.4f, 0.32f, 0.26f));
		AddBox(root, "BenchE", new Vector3(4.5f, 0.35f, -3f), new Vector3(1.8f, 0.4f, 0.55f),
			new Color(0.4f, 0.32f, 0.26f));

		AddBox(root, "SpawnPad", new Vector3(site.SpawnEye.X, 0.04f, site.SpawnEye.Z),
			new Vector3(1.6f, 0.06f, 1.6f), new Color(0.35f, 0.45f, 0.55f));

		var label = new Label3D
		{
			Name = "SiteLabel",
			Text = $"{site.Name}\n({site.Kind})",
			Position = new Vector3(0f, 3.4f, -7f),
			FontSize = 48,
			Modulate = new Color(0.92f, 0.86f, 0.7f),
			Billboard = BaseMaterial3D.BillboardModeEnum.Enabled,
		};
		root.AddChild(label);

		return root;
	}

	private static void AddBox(Node3D parent, string name, Vector3 pos, Vector3 size, Color color)
	{
		var mesh = new MeshInstance3D { Name = name, Position = pos };
		mesh.Mesh = new BoxMesh { Size = size };
		mesh.MaterialOverride = new StandardMaterial3D
		{
			AlbedoColor = color,
			Roughness = 0.85f,
		};
		parent.AddChild(mesh);
	}

	private static void AddPillar(Node3D parent, string name, Vector3 pos, Color color)
	{
		AddBox(parent, name, pos, new Vector3(0.35f, 1.4f, 0.35f), color);
	}
}
