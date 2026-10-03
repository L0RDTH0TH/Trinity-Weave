using System;
using System.Collections.Generic;
using Genesis.Core.ClosedAlpha;
using Godot;

namespace Genesis.UI;

/// <summary>
/// Depth-1 ux_worldgen_gui host — collaborative propose / refine / preview / accept.
/// Presentation-only: emits intent signals; never mutates WorldShell / sim.
/// </summary>
public partial class WorldgenGui : Control
{
	[Signal]
	public delegate void ScaffoldAcceptedEventHandler(string scaffoldId, string toneProfile);

	[Signal]
	public delegate void DialogueCancelledEventHandler();

	private static readonly (string Id, string Tone, string Title, string Preview)[] Scaffolds =
	{
		("pastoral_valleys", "Pastoral", "Pastoral valleys",
			"Soft hills, settlement clearings, mild weather bias — blank craft start with pastoral tone tags."),
		("grimdark_marches", "Grimdark", "Grimdark marches",
			"Harsh ridges, scarred roads, costly hope — blank craft start with grimdark tone tags."),
		("verdant_frontier", "Verdant", "Verdant frontier",
			"Dense green belts, oasis-ready desert edge — blank craft start with verdant tone tags."),
	};

	private Label? _previewLabel;
	private Label? _headerLabel;
	private Label? _refuseLabel;
	private VBoxContainer? _optionStack;
	private int _selectedIndex;
	private int _refineStep;
	private bool _seatAllowed = true;

	/// <summary>Presentation seat gate — Player cannot author the first world.</summary>
	[Export]
	public bool AllowPlayerAuthoring { get; set; }

	public override void _Ready()
	{
		AlphaFactoryLog.ConfigureRuntimePath();

		_previewLabel = GetNodeOrNull<Label>("%PreviewBody");
		_headerLabel = GetNodeOrNull<Label>("%HeaderLabel");
		_refuseLabel = GetNodeOrNull<Label>("%RefuseLabel");
		_optionStack = GetNodeOrNull<VBoxContainer>("%OptionStack");

		var propose = GetNodeOrNull<Button>("%ProposeButton");
		var refine = GetNodeOrNull<Button>("%RefineButton");
		var accept = GetNodeOrNull<Button>("%AcceptButton");
		var regenerate = GetNodeOrNull<Button>("%RegenerateButton");
		var cancel = GetNodeOrNull<Button>("%CancelButton");

		if (propose != null) propose.Pressed += OnPropose;
		if (refine != null) refine.Pressed += OnRefine;
		if (accept != null) accept.Pressed += OnAccept;
		if (regenerate != null) regenerate.Pressed += OnRegenerate;
		if (cancel != null) cancel.Pressed += OnCancel;

		EnforceSeatGuard();
		RebuildOptions();
		RefreshPreview();

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"ux_worldgen_gui entered — collaborative generation dialogue armed",
			new Dictionary<string, object>
			{
				["slice_id"] = "row_ux_world_generation_r1_d1",
				["lane_id"] = "presentation",
				["ux_bullet"] = "UX-1",
				["surface"] = "ux_worldgen_gui",
				["checklist"] = new[] { "Flow_Launch", "Anti_DevOnlyHUD", "Flow_DM_Mode" },
			});
	}

	public void SetSeatAllowed(bool allowed)
	{
		_seatAllowed = allowed;
		EnforceSeatGuard();
	}

	private void EnforceSeatGuard()
	{
		var ok = _seatAllowed && !AllowPlayerAuthoring;
		if (_refuseLabel != null)
		{
			_refuseLabel.Visible = !ok;
			_refuseLabel.Text = ok
				? string.Empty
				: "Wrong seat — players do not author the first world. DM / shared table only.";
		}

		foreach (var path in new[] { "%ProposeButton", "%RefineButton", "%AcceptButton", "%RegenerateButton" })
		{
			var btn = GetNodeOrNull<Button>(path);
			if (btn != null) btn.Disabled = !ok;
		}

		if (!ok)
		{
			AlphaFactoryLog.Emit(
				"ui.refuse",
				"Anti_DevOnlyHUD",
				"ux_worldgen_gui refused — wrong seat / player authoring blocked",
				level: "warn");
		}
	}

	private void RebuildOptions()
	{
		if (_optionStack == null) return;
		foreach (var child in _optionStack.GetChildren())
			child.QueueFree();

		for (var i = 0; i < Scaffolds.Length; i++)
		{
			var index = i;
			var scaffold = Scaffolds[i];
			var btn = new Button
			{
				Text = scaffold.Title,
				ToggleMode = true,
				ButtonPressed = i == _selectedIndex,
				CustomMinimumSize = new Vector2(0, 36),
			};
			ApplyBronzeButton(btn, selected: i == _selectedIndex);
			btn.Pressed += () => SelectScaffold(index);
			_optionStack.AddChild(btn);
		}
	}

	private void SelectScaffold(int index)
	{
		_selectedIndex = Math.Clamp(index, 0, Scaffolds.Length - 1);
		_refineStep = 0;
		RebuildOptions();
		RefreshPreview();
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_DM_Mode",
			$"Scaffold chosen — {Scaffolds[_selectedIndex].Id}",
			new Dictionary<string, object>
			{
				["scaffold_id"] = Scaffolds[_selectedIndex].Id,
				["tone"] = Scaffolds[_selectedIndex].Tone,
			});
	}

	private void RefreshPreview()
	{
		var s = Scaffolds[_selectedIndex];
		var refineNote = _refineStep switch
		{
			0 => "Preview: initial scaffold proposal (not yet durable).",
			1 => "Refined: favor settlement clearings + soft biome edges.",
			2 => "Refined: favor monster-region tags on the rim.",
			_ => "Refined: favor import/attach-ready blank canvas.",
		};

		if (_headerLabel != null)
			_headerLabel.Text = $"WORLDGEN · {s.Tone.ToUpperInvariant()}";

		if (_previewLabel != null)
			_previewLabel.Text =
				$"{s.Preview}\n\n{refineNote}\n\nAccept commits presentation intent only — craft cam authors cells; F5 persists the living world.";
	}

	private void OnPropose()
	{
		_selectedIndex = (_selectedIndex + 1) % Scaffolds.Length;
		_refineStep = 0;
		RebuildOptions();
		RefreshPreview();
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			$"Proposed scaffold family — {Scaffolds[_selectedIndex].Id}");
	}

	private void OnRefine()
	{
		_refineStep = (_refineStep + 1) % 4;
		RefreshPreview();
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_DM_Mode",
			$"Refined scaffold preview step={_refineStep}");
	}

	private void OnRegenerate()
	{
		_selectedIndex = (_selectedIndex + Scaffolds.Length - 1) % Scaffolds.Length;
		_refineStep = 0;
		RebuildOptions();
		RefreshPreview();
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			$"Regenerate requested — now {Scaffolds[_selectedIndex].Id}");
	}

	private void OnAccept()
	{
		if (!_seatAllowed || AllowPlayerAuthoring)
		{
			EnforceSeatGuard();
			return;
		}

		var s = Scaffolds[_selectedIndex];
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Anti_DevOnlyHUD",
			"Worldgen accept — presentation intent for durable living world (no sim write)",
			new Dictionary<string, object>
			{
				["scaffold_id"] = s.Id,
				["tone"] = s.Tone,
				["refine_step"] = _refineStep,
				["ux_bullet"] = "UX-1",
			});

		EmitSignal(SignalName.ScaffoldAccepted, s.Id, s.Tone);
	}

	private void OnCancel()
	{
		AlphaFactoryLog.Emit("ui.boundary", "Flow_Launch", "ux_worldgen_gui cancelled");
		EmitSignal(SignalName.DialogueCancelled);
	}

	private static void ApplyBronzeButton(Button btn, bool selected)
	{
		var normal = new StyleBoxFlat
		{
			BgColor = selected ? new Color(0.55f, 0.52f, 0.48f, 1f) : new Color(0.28f, 0.22f, 0.16f, 1f),
			BorderColor = new Color(0.72f, 0.58f, 0.32f, 1f),
			BorderWidthLeft = 2,
			BorderWidthTop = 2,
			BorderWidthRight = 2,
			BorderWidthBottom = 2,
			CornerRadiusTopLeft = 4,
			CornerRadiusTopRight = 4,
			CornerRadiusBottomRight = 4,
			CornerRadiusBottomLeft = 4,
			ContentMarginLeft = 12,
			ContentMarginRight = 12,
			ContentMarginTop = 8,
			ContentMarginBottom = 8,
		};
		btn.AddThemeStyleboxOverride("normal", normal);
		btn.AddThemeStyleboxOverride("pressed", normal);
		btn.AddThemeStyleboxOverride("hover", normal);
		btn.AddThemeColorOverride("font_color", new Color(0.95f, 0.93f, 0.88f));
	}
}
