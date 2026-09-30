using Godot;

namespace Genesis.Place;

/// <summary>Builds a readable shrine courtyard — path, walls, landmark. Placeholder art only.</summary>
public static class ShrineCourtyardBuilder
{
	public static Node3D Build(Node3D parent)
	{
		var root = new Node3D { Name = "ShrineCourtyard" };
		parent.AddChild(root);

		var env = new Godot.Environment
		{
			BackgroundMode = Godot.Environment.BGMode.Color,
			BackgroundColor = new Color(0.18f, 0.22f, 0.32f),
			AmbientLightSource = Godot.Environment.AmbientSource.Color,
			AmbientLightColor = new Color(0.45f, 0.48f, 0.55f),
			TonemapMode = Godot.Environment.ToneMapper.Filmic,
		};
		root.AddChild(new WorldEnvironment { Environment = env });

		var sun = new DirectionalLight3D
		{
			Name = "Sun",
			RotationDegrees = new Vector3(-42f, 28f, 0f),
			LightEnergy = 1.15f,
			ShadowEnabled = false,
		};
		root.AddChild(sun);

		// Ground plane — courtyard floor
		AddBox(root, "Floor", new Vector3(0f, -0.15f, -2f), new Vector3(22f, 0.3f, 28f),
			new Color(0.26f, 0.30f, 0.28f));

		// Stone path from spawn (south) toward shrine (north)
		AddBox(root, "Path", new Vector3(0f, 0.02f, 1f), new Vector3(2.4f, 0.08f, 16f),
			new Color(0.42f, 0.38f, 0.34f));

		// Low courtyard walls
		AddBox(root, "WallWest", new Vector3(-7f, 1.0f, -1f), new Vector3(0.45f, 2.0f, 20f),
			new Color(0.34f, 0.33f, 0.36f));
		AddBox(root, "WallEast", new Vector3(7f, 1.0f, -1f), new Vector3(0.45f, 2.0f, 20f),
			new Color(0.34f, 0.33f, 0.36f));
		AddBox(root, "WallNorth", new Vector3(0f, 1.0f, -11f), new Vector3(14.5f, 2.0f, 0.45f),
			new Color(0.32f, 0.31f, 0.34f));

		// Path lanterns (readable depth cues)
		AddPillar(root, "LanternL1", new Vector3(-1.6f, 0.7f, 5f), new Color(0.75f, 0.55f, 0.25f));
		AddPillar(root, "LanternR1", new Vector3(1.6f, 0.7f, 5f), new Color(0.75f, 0.55f, 0.25f));
		AddPillar(root, "LanternL2", new Vector3(-1.6f, 0.7f, 0f), new Color(0.7f, 0.5f, 0.22f));
		AddPillar(root, "LanternR2", new Vector3(1.6f, 0.7f, 0f), new Color(0.7f, 0.5f, 0.22f));

		// Landmark shrine at path end
		var shrine = new Node3D { Name = "Shrine", Position = new Vector3(0f, 0f, -8f) };
		root.AddChild(shrine);
		AddBox(shrine, "Plinth", new Vector3(0f, 0.35f, 0f), new Vector3(3.2f, 0.7f, 2.4f),
			new Color(0.48f, 0.44f, 0.40f));
		AddBox(shrine, "Stele", new Vector3(0f, 1.8f, 0f), new Vector3(1.1f, 2.4f, 0.55f),
			new Color(0.62f, 0.52f, 0.38f));
		AddBox(shrine, "Crown", new Vector3(0f, 3.15f, 0f), new Vector3(1.6f, 0.35f, 0.7f),
			new Color(0.78f, 0.62f, 0.32f));

		// Side alcove benches
		AddBox(root, "BenchW", new Vector3(-4.5f, 0.35f, -3f), new Vector3(1.8f, 0.4f, 0.55f),
			new Color(0.4f, 0.32f, 0.26f));
		AddBox(root, "BenchE", new Vector3(4.5f, 0.35f, -3f), new Vector3(1.8f, 0.4f, 0.55f),
			new Color(0.4f, 0.32f, 0.26f));

		// Spawn marker ring (subtle)
		AddBox(root, "SpawnPad", new Vector3(0f, 0.04f, 7.5f), new Vector3(1.6f, 0.06f, 1.6f),
			new Color(0.35f, 0.45f, 0.55f));

		return root;
	}

	public static Vector3 SpawnEyePosition => new(0f, 1.65f, 7.5f);

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
