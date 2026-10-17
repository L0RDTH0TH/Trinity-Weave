using System;
using System.Collections.Generic;
using Genesis.Core.ClosedAlpha;
using Genesis.Core.WorldGen;
using Godot;

namespace Genesis.UI;

/// <summary>
/// Create World path: bias → dials → scaffold propose/accept → optional lore → Open (auto-gen).
/// WORLD-s0 optional lore: DM (+ Shared table note) freeform skip-ok; filled salts gen.
/// No Player freeform — PCs attach later from friends/sheets (parked). Never Accept≥1 gate.
/// Layout chrome deferred to sibling (no anchors/ScrollContainer edits).
/// </summary>
public partial class WorldgenGui : Control
{
	[Signal]
	public delegate void ScaffoldAcceptedEventHandler(string scaffoldId, string toneProfile);

	[Signal]
	public delegate void DialogueCancelledEventHandler();

	private enum Phase
	{
		Bias = 0,
		Bounds = 1,
		Propose = 2,
		Intents = 3,
	}

	private static readonly (string Id, string Label, string Title, string Preview)[] GenBiases =
	{
		("high", "High", "High Fantasy bias",
			"Default gen bias: brighter myth, clearer heroes, kinder landfall — campaigns may later bind/override ToneProfile."),
		("medium", "Medium", "Medium Fantasy bias",
			"Default gen bias: Exemplar-shaped middle road — campaigns may later bind/override ToneProfile."),
		("low", "Low", "Low Fantasy bias",
			"Default gen bias: scarce wonder, harder logistics — campaigns may later bind/override ToneProfile."),
		("grimdark", "Grimdark", "Grimdark bias",
			"Default gen bias: costly hope, scarred roads — campaigns may later bind/override ToneProfile."),
	};

	private static readonly (string Key, string Label, float Min, float Max, float Step)[] DialSpecs =
	{
		("cell_size", "Cell size", WorldBoundsDials.CellSizeMin, WorldBoundsDials.CellSizeMax, 0.05f),
		("cell_count", "Cell count", WorldBoundsDials.CellCountMin, WorldBoundsDials.CellCountMax, 1f),
		("settlement_distance", "Settlement distance", WorldBoundsDials.SettlementMin, WorldBoundsDials.SettlementMax, 0.05f),
		("rivers", "Rivers", WorldBoundsDials.RiversMin, WorldBoundsDials.RiversMax, 0.05f),
		("climate", "Climate", WorldBoundsDials.ClimateMin, WorldBoundsDials.ClimateMax, 0.05f),
		("wildness", "Wildness", WorldBoundsDials.WildnessMin, WorldBoundsDials.WildnessMax, 0.05f),
	};

	private Label? _previewLabel;
	private Label? _headerLabel;
	private Label? _refuseLabel;
	private VBoxContainer? _optionStack;
	private Button? _proposeButton;
	private Button? _refineButton;
	private Button? _regenerateButton;
	private Button? _acceptButton;
	private int _selectedIndex = 1; // Medium default
	private int _refineStep;
	private int _proposeRevision;
	private int _reviseSalt;
	private bool _seatAllowed = true;
	private Phase _phase = Phase.Bias;
	private WorldBoundsDials _dials = WorldBoundsDials.Defaults;
	private WorldScaffoldProposal _scaffold = WorldScaffoldProposal.Empty;
	private WorldSession0IntentBoard _intents = WorldSession0IntentBoard.Empty;
	private string _loreDm = "";
	private string _loreShared = "";
	private readonly Dictionary<string, HSlider> _sliders = new();

	/// <summary>Feedstock dials selected on Accept (LaunchShell reads after signal).</summary>
	public WorldBoundsDials SelectedDials => _dials;

	/// <summary>Accepted (or last proposed) scaffold for package bind.</summary>
	public WorldScaffoldProposal SelectedScaffold => _scaffold;

	/// <summary>Optional world-seed / lore board (empty = Open skip-ok; filled salts gen).</summary>
	public WorldSession0IntentBoard SelectedIntents => _intents;

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

		_proposeButton = GetNodeOrNull<Button>("%ProposeButton");
		_refineButton = GetNodeOrNull<Button>("%RefineButton");
		_acceptButton = GetNodeOrNull<Button>("%AcceptButton");
		_regenerateButton = GetNodeOrNull<Button>("%RegenerateButton");
		var cancel = GetNodeOrNull<Button>("%CancelButton");

		if (_proposeButton != null)
			_proposeButton.Pressed += OnPropose;
		if (_refineButton != null)
			_refineButton.Pressed += OnRefine;
		if (_acceptButton != null)
			_acceptButton.Pressed += OnAccept;
		if (_regenerateButton != null)
			_regenerateButton.Pressed += OnRegenerate;
		if (cancel != null) cancel.Pressed += OnCancel;

		EnforceSeatGuard();
		EnterPhase(Phase.Bias);

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"Create World dialogue armed — bias → dials → scaffold → optional lore → Open",
			new Dictionary<string, object>
			{
				["slice_id"] = WorldPackage.SliceId,
				["s0_packaging_slice"] = WorldSession0IntentBoard.PackagingSliceId,
				["s0_optional_lore_slice"] = WorldSession0IntentBoard.OptionalLoreSliceId,
				["s0_dm_lore_honesty_slice"] = WorldSession0IntentBoard.DmLoreHonestySliceId,
				["ask_id"] = WorldPackage.AskId,
				["ticket_map"] = WorldPackage.TicketMap,
				["prior_keep"] = WorldPackage.PriorKeepSliceId,
				["lane_id"] = "presentation",
				["ux_bullet"] = "UX-1",
				["surface"] = "ux_worldgen_gui",
				["claim_class"] = "staging",
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
				: "Wrong seat — players do not author the first world (may seed Session 0 intents). DM opens.";
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
				"WORLD-s0-intents refused — wrong seat / player world-authoring blocked",
				level: "warn");
		}
	}

	private void EnterPhase(Phase phase)
	{
		_phase = phase;
		_refineStep = 0;
		if (phase == Phase.Propose)
		{
			_proposeRevision = 0;
			_reviseSalt = 0;
			MintProposal(forceNew: true);
		}
		else if (phase == Phase.Intents)
		{
			// Optional lore capture — start empty; never SeedFor Accept≥1 bank.
			_intents = WorldSession0IntentBoard.Empty;
		}

		RebuildPhaseChrome();
		RebuildOptions();
		RefreshPreview();
	}

	private void RebuildPhaseChrome()
	{
		if (_phase == Phase.Bias)
		{
			if (_proposeButton != null) _proposeButton.Text = "Next bias";
			if (_refineButton != null) _refineButton.Text = "Note";
			if (_regenerateButton != null) _regenerateButton.Text = "Prev bias";
			if (_acceptButton != null) _acceptButton.Text = "Set bounds →";
		}
		else if (_phase == Phase.Bounds)
		{
			if (_proposeButton != null) _proposeButton.Text = "Reset dials";
			if (_refineButton != null) _refineButton.Text = "Note";
			if (_regenerateButton != null) _regenerateButton.Text = "← Bias";
			if (_acceptButton != null) _acceptButton.Text = "Propose scaffold →";
		}
		else if (_phase == Phase.Propose)
		{
			if (_proposeButton != null) _proposeButton.Text = "Propose again";
			if (_refineButton != null) _refineButton.Text = "Revise";
			if (_regenerateButton != null) _regenerateButton.Text = "Reject";
			if (_acceptButton != null) _acceptButton.Text = "Accept scaffold →";
		}
		else
		{
			if (_proposeButton != null) _proposeButton.Text = "Clear lore";
			if (_refineButton != null) _refineButton.Text = "Tip";
			if (_regenerateButton != null) _regenerateButton.Text = "← Scaffold";
			if (_acceptButton != null) _acceptButton.Text = "Open world →";
		}
	}

	private void RebuildOptions()
	{
		if (_optionStack == null) return;
		foreach (var child in _optionStack.GetChildren())
			child.QueueFree();
		_sliders.Clear();

		if (_phase == Phase.Bias)
			RebuildBiasOptions();
		else if (_phase == Phase.Bounds)
			RebuildDialOptions();
		else if (_phase == Phase.Propose)
			RebuildProposeStatus();
		else
			RebuildOptionalLoreOptions();
	}

	private void RebuildBiasOptions()
	{
		if (_optionStack == null) return;
		for (var i = 0; i < GenBiases.Length; i++)
		{
			var index = i;
			var bias = GenBiases[i];
			var btn = new Button
			{
				Text = bias.Title,
				ToggleMode = true,
				ButtonPressed = i == _selectedIndex,
				CustomMinimumSize = new Vector2(0, 36),
			};
			ApplyBronzeButton(btn, selected: i == _selectedIndex);
			btn.Pressed += () => SelectBias(index);
			_optionStack.AddChild(btn);
		}
	}

	private void RebuildDialOptions()
	{
		if (_optionStack == null) return;
		var values = new Dictionary<string, float>
		{
			["cell_size"] = _dials.CellSize,
			["cell_count"] = _dials.CellCount,
			["settlement_distance"] = _dials.SettlementDistance,
			["rivers"] = _dials.Rivers,
			["climate"] = _dials.Climate,
			["wildness"] = _dials.Wildness,
		};

		foreach (var spec in DialSpecs)
		{
			var row = new VBoxContainer { CustomMinimumSize = new Vector2(0, 48) };
			var header = new HBoxContainer();
			var label = new Label
			{
				Text = spec.Label,
				SizeFlagsHorizontal = Control.SizeFlags.ExpandFill,
			};
			label.AddThemeColorOverride("font_color", new Color(0.92f, 0.9f, 0.84f));
			var valueLabel = new Label { Text = values[spec.Key].ToString("0.##") };
			valueLabel.AddThemeColorOverride("font_color", new Color(0.72f, 0.58f, 0.32f));
			header.AddChild(label);
			header.AddChild(valueLabel);
			row.AddChild(header);

			var slider = new HSlider
			{
				MinValue = spec.Min,
				MaxValue = spec.Max,
				Step = spec.Step,
				Value = values[spec.Key],
				SizeFlagsHorizontal = Control.SizeFlags.ExpandFill,
				CustomMinimumSize = new Vector2(0, 18),
			};
			var key = spec.Key;
			slider.ValueChanged += v => OnDialChanged(key, (float)v, valueLabel);
			_sliders[key] = slider;
			row.AddChild(slider);
			_optionStack.AddChild(row);
		}
	}

	private void RebuildProposeStatus()
	{
		if (_optionStack == null) return;
		var status = new Label
		{
			Text = _scaffold.CanAccept
				? $"PROPOSED · rev {_scaffold.Revision} · {_scaffold.ScaffoldId}"
				: _scaffold.Status == WorldScaffoldProposal.Disposition.Rejected
					? "REJECTED — Propose again before Accept"
					: "EMPTY — Propose a scaffold first",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
		};
		status.AddThemeColorOverride(
			"font_color",
			_scaffold.CanAccept
				? new Color(0.75f, 0.88f, 0.62f)
				: new Color(1f, 0.78f, 0.55f));
		_optionStack.AddChild(status);

		var keep = new Label
		{
			Text = "Loop: Propose again · Revise · Reject · Accept → Open feeds gen (salt changes land/water). Menu-only barred.",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
		};
		keep.AddThemeColorOverride("font_color", new Color(0.78f, 0.76f, 0.7f));
		_optionStack.AddChild(keep);
	}

	private void RebuildOptionalLoreOptions()
	{
		if (_optionStack == null) return;
		var summary = new Label
		{
			Text = "Optional DM world lore / seeds — leave blank and Open still works.",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
		};
		summary.AddThemeColorOverride("font_color", new Color(0.75f, 0.88f, 0.62f));
		_optionStack.AddChild(summary);

		var stub = new Label
		{
			Text = "Player characters attach later from friends / character sheets (not typed here).",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
		};
		stub.AddThemeColorOverride("font_color", new Color(0.72f, 0.8f, 0.9f));
		_optionStack.AddChild(stub);

		AddLoreField(
			"DM (optional)",
			"DM we start in Magic France…",
			_loreDm,
			v =>
			{
				_loreDm = v;
				RefreshLorePreviewOnly();
			});
		AddLoreField(
			"Shared (optional)",
			"Table / world note that biases the world…",
			_loreShared,
			v =>
			{
				_loreShared = v;
				RefreshLorePreviewOnly();
			});

		var tip = new Label
		{
			Text = "Filled DM/Shared salt Create World Open gen (like Propose Accept). Empty = same as skip.",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
		};
		tip.AddThemeColorOverride("font_color", new Color(0.78f, 0.76f, 0.7f));
		_optionStack.AddChild(tip);
	}

	private void AddLoreField(string label, string placeholder, string current, Action<string> onChanged)
	{
		if (_optionStack == null) return;
		var row = new VBoxContainer { CustomMinimumSize = new Vector2(0, 56) };
		var hdr = new Label { Text = label };
		hdr.AddThemeColorOverride("font_color", new Color(0.92f, 0.9f, 0.84f));
		row.AddChild(hdr);
		var edit = new LineEdit
		{
			Text = current,
			PlaceholderText = placeholder,
			SizeFlagsHorizontal = Control.SizeFlags.ExpandFill,
			CustomMinimumSize = new Vector2(0, 28),
		};
		// Godot LineEdit.TextChangedEventHandler is not Action<string> — wrap or CS build fails (F5 no-launch).
		edit.TextChanged += newText => onChanged(newText);
		row.AddChild(edit);
		_optionStack.AddChild(row);
	}

	private void RefreshLorePreviewOnly()
	{
		_intents = WorldSession0IntentBoard.FromOptionalLore(
			_loreDm, _loreShared, _scaffold.ScaffoldId);
		RefreshPreview();
	}

	private void ClearOptionalLore()
	{
		_loreDm = "";
		_loreShared = "";
		_intents = WorldSession0IntentBoard.Empty;
		RebuildOptions();
		RefreshPreview();
	}

	private void OnDialChanged(string key, float value, Label valueLabel)
	{
		valueLabel.Text = key == "cell_count"
			? ((int)Math.Round(value)).ToString()
			: value.ToString("0.##");
		_dials = key switch
		{
			"cell_size" => _dials.With(cellSize: value),
			"cell_count" => _dials.With(cellCount: value),
			"settlement_distance" => _dials.With(settlementDistance: value),
			"rivers" => _dials.With(rivers: value),
			"climate" => _dials.With(climate: value),
			"wildness" => _dials.With(wildness: value),
			_ => _dials,
		};
		RefreshPreview();
	}

	private void SelectBias(int index)
	{
		_selectedIndex = Math.Clamp(index, 0, GenBiases.Length - 1);
		_refineStep = 0;
		RebuildOptions();
		RefreshPreview();
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_DM_Mode",
			$"Gen bias chosen — {GenBiases[_selectedIndex].Id}",
			new Dictionary<string, object>
			{
				["gen_bias"] = GenBiases[_selectedIndex].Id,
				["ask_id"] = WorldPackage.AskId,
			});
	}

	private void MintProposal(bool forceNew)
	{
		if (forceNew || !_scaffold.CanAccept)
			_proposeRevision++;
		else
			_proposeRevision = Math.Max(1, _proposeRevision + 1);

		var bias = GenBiases[_selectedIndex].Id;
		_scaffold = WorldScaffoldProposal.Propose(bias, _dials, _proposeRevision, _reviseSalt);
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_DM_Mode",
			$"WORLD-propose minted — {_scaffold.ScaffoldId} rev={_scaffold.Revision}",
			_scaffold.ToLogFields());
	}

	private void RefreshPreview()
	{
		if (_phase == Phase.Bias)
		{
			var s = GenBiases[_selectedIndex];
			var refineNote = _refineStep switch
			{
				0 => "WORLD-new KEEP: pick default gen bias, then Set bounds for feedstock dials.",
				1 => "Note: ToneProfile remains campaign-bindable later — this bias is world default only.",
				2 => "Note: WORLD-bounds dials bias later GEN — Accept does not fill the map.",
				_ => "Note: WORLD-propose next — tool scaffold, DM accept/reject/revise.",
			};

			if (_headerLabel != null)
				_headerLabel.Text = $"WORLD-NEW · {s.Label.ToUpperInvariant()}";

			if (_previewLabel != null)
				_previewLabel.Text =
					$"{s.Preview}\n\n{refineNote}\n\nNext: Set bounds → dials → Propose scaffold.";
			return;
		}

		if (_phase == Phase.Bounds)
		{
			var bias = GenBiases[_selectedIndex];
			var dialNote = _refineStep switch
			{
				0 => "WORLD-bounds: Cell size = landform scale; Cell count = seed rings / board cells (sister dials).",
				1 => "Note: higher Cell count → more cells on Create World Open; Cell size coarsens continents.",
				2 => "Note: rivers/climate/wildness + size/count change the Open gen pass (W2).",
				_ => "Note: Propose scaffold → then Session 0 intents → Open world.",
			};

			if (_headerLabel != null)
				_headerLabel.Text = $"WORLD-BOUNDS · {bias.Label.ToUpperInvariant()}";

			if (_previewLabel != null)
				_previewLabel.Text =
					$"Bias={bias.Id}\nDials: {_dials.SummaryLine()}\n\n{dialNote}\n\nPropose scaffold → tool proposes; DM accepts / rejects / revises.";
			return;
		}

		if (_phase == Phase.Propose)
		{
			var biasId = GenBiases[_selectedIndex].Id;
			if (_headerLabel != null)
				_headerLabel.Text = $"WORLD-PROPOSE · {biasId.ToUpperInvariant()} · REV {_scaffold.Revision}";

			if (_previewLabel != null)
				_previewLabel.Text = _scaffold.PreviewBody()
					+ "\n\nAccept scaffold → optional lore (skip-ok) → Open world (Create World auto-gen).";
			return;
		}

		// Optional lore phase
		if (_headerLabel != null)
			_headerLabel.Text =
				$"WORLD-S0-LORE · OPTIONAL · {GenBiases[_selectedIndex].Id.ToUpperInvariant()}"
				+ (_intents.LoreFed ? $" · SALT 0x{_intents.LoreFeedSalt:x8}" : " · EMPTY");

		if (_previewLabel != null)
			_previewLabel.Text = _intents.PreviewBody();
	}

	private void OnPropose()
	{
		if (_phase == Phase.Bias)
		{
			_selectedIndex = (_selectedIndex + 1) % GenBiases.Length;
			_refineStep = 0;
			RebuildOptions();
			RefreshPreview();
			AlphaFactoryLog.Emit(
				"ui.boundary",
				"Flow_Launch",
				$"Next gen bias — {GenBiases[_selectedIndex].Id}");
			return;
		}

		if (_phase == Phase.Bounds)
		{
			_dials = WorldBoundsDials.Defaults;
			RebuildOptions();
			RefreshPreview();
			AlphaFactoryLog.Emit("ui.boundary", "Flow_Launch", "WORLD-bounds dials reset to defaults");
			return;
		}

		if (_phase == Phase.Propose)
		{
			// Propose again — new revision (not one-shot).
			_reviseSalt = 0;
			MintProposal(forceNew: true);
			RebuildOptions();
			RefreshPreview();
			return;
		}

		// Optional lore: Clear lore.
		ClearOptionalLore();
		if (_refuseLabel != null) _refuseLabel.Visible = false;
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_DM_Mode",
			"WORLD-s0 optional lore cleared — Open still skip-ok",
			WorldSession0IntentBoard.Empty.ToLogFields());
	}

	private void OnRefine()
	{
		if (_phase == Phase.Intents)
		{
			_refineStep = (_refineStep + 1) % 4;
			RefreshPreview();
			AlphaFactoryLog.Emit(
				"ui.boundary",
				"Flow_DM_Mode",
				$"WORLD-s0 optional lore tip step={_refineStep}");
			return;
		}

		if (_phase != Phase.Propose)
		{
			_refineStep = (_refineStep + 1) % 4;
			RefreshPreview();
			AlphaFactoryLog.Emit(
				"ui.boundary",
				"Flow_DM_Mode",
				$"WORLD note step={_refineStep} phase={_phase}");
			return;
		}

		// Revise: bump salt and remint same revision family.
		_reviseSalt++;
		_scaffold = WorldScaffoldProposal.Propose(
			GenBiases[_selectedIndex].Id,
			_dials,
			Math.Max(1, _proposeRevision),
			_reviseSalt);
		RebuildOptions();
		RefreshPreview();
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_DM_Mode",
			$"WORLD-propose revise salt={_reviseSalt} → {_scaffold.ScaffoldId}",
			_scaffold.ToLogFields());
	}

	private void OnRegenerate()
	{
		if (_phase == Phase.Bias)
		{
			_selectedIndex = (_selectedIndex + GenBiases.Length - 1) % GenBiases.Length;
			_refineStep = 0;
			RebuildOptions();
			RefreshPreview();
			AlphaFactoryLog.Emit(
				"ui.boundary",
				"Flow_Launch",
				$"Prev gen bias — {GenBiases[_selectedIndex].Id}");
			return;
		}

		if (_phase == Phase.Bounds)
		{
			EnterPhase(Phase.Bias);
			AlphaFactoryLog.Emit("ui.boundary", "Flow_Launch", "WORLD-bounds returned to bias phase");
			return;
		}

		if (_phase == Phase.Propose)
		{
			// Reject current scaffold — must Propose again before Accept.
			_scaffold = _scaffold.Status == WorldScaffoldProposal.Disposition.Empty
				? WorldScaffoldProposal.Empty
				: _scaffold.AsRejected();
			RebuildOptions();
			RefreshPreview();
			AlphaFactoryLog.Emit(
				"ui.boundary",
				"Flow_DM_Mode",
				$"WORLD-propose rejected — {_scaffold.ScaffoldId}",
				_scaffold.ToLogFields());
			return;
		}

		// Optional lore: back to scaffold propose (re-mint keep path honest).
		EnterPhase(Phase.Propose);
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_DM_Mode",
			"WORLD-s0 optional lore returned to scaffold propose");
	}

	private void OnAccept()
	{
		if (!_seatAllowed || AllowPlayerAuthoring)
		{
			EnforceSeatGuard();
			return;
		}

		if (_phase == Phase.Bias)
		{
			EnterPhase(Phase.Bounds);
			AlphaFactoryLog.Emit(
				"ui.boundary",
				"Flow_DM_Mode",
				$"WORLD-bounds phase — bias={GenBiases[_selectedIndex].Id}",
				new Dictionary<string, object>
				{
					["gen_bias"] = GenBiases[_selectedIndex].Id,
					["ask_id"] = WorldPackage.AskId,
				});
			return;
		}

		if (_phase == Phase.Bounds)
		{
			EnterPhase(Phase.Propose);
			AlphaFactoryLog.Emit(
				"ui.boundary",
				"Flow_DM_Mode",
				$"WORLD-propose phase — bias={GenBiases[_selectedIndex].Id} dials=[{_dials.SummaryLine()}]",
				new Dictionary<string, object>
				{
					["gen_bias"] = GenBiases[_selectedIndex].Id,
					["ask_id"] = WorldPackage.AskId,
					["dials_summary"] = _dials.SummaryLine(),
					["scaffold_id"] = _scaffold.ScaffoldId,
				});
			return;
		}

		if (_phase == Phase.Propose)
		{
			if (!_scaffold.CanAccept)
			{
				if (_refuseLabel != null)
				{
					_refuseLabel.Visible = true;
					_refuseLabel.Text = "No proposed scaffold — Propose again (or Revise) before Accept.";
				}

				AlphaFactoryLog.Emit(
					"ui.refuse",
					"Anti_DevOnlyHUD",
					"WORLD-propose Accept blocked — scaffold not in proposed state",
					new Dictionary<string, object>
					{
						["scaffold_status"] = _scaffold.Status.ToString().ToLowerInvariant(),
					},
					level: "warn");
				return;
			}

			_scaffold = _scaffold.AsAccepted();
			// Optional lore phase — skip-ok; never Accept≥1 gate; Open always lawful.
			_loreDm = "";
			_loreShared = "";
			_intents = WorldSession0IntentBoard.Empty;
			AlphaFactoryLog.Emit(
				"ui.boundary",
				"Flow_DM_Mode",
				$"WORLD-propose accepted — optional lore (skip-ok) · scaffold={_scaffold.ScaffoldId}",
				_scaffold.ToLogFields());
			EnterPhase(Phase.Intents);
			return;
		}

		// Optional lore Open — always lawful (empty or filled). DM (+ Shared) only.
		_intents = WorldSession0IntentBoard.FromOptionalLore(
			_loreDm, _loreShared, _scaffold.ScaffoldId);
		if (_refuseLabel != null) _refuseLabel.Visible = false;
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_DM_Mode",
			_intents.LoreFed
				? $"WORLD-s0 optional lore Open — salt=0x{_intents.LoreFeedSalt:x8}"
				: "WORLD-s0 optional lore Open — empty skip-ok",
			_intents.ToLogFields());
		EmitOpenWorld();
	}

	private void EmitOpenWorld()
	{
		var s = GenBiases[_selectedIndex];
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Anti_DevOnlyHUD",
			"Create World open — bias + dials + scaffold + optional lore (empty skip-ok; filled salts gen)",
			new Dictionary<string, object>
			{
				["gen_bias"] = s.Id,
				["refine_step"] = _refineStep,
				["ask_id"] = WorldPackage.AskId,
				["slice_id"] = WorldPackage.SliceId,
				["s0_packaging_slice"] = WorldSession0IntentBoard.PackagingSliceId,
				["s0_optional_lore_slice"] = WorldSession0IntentBoard.OptionalLoreSliceId,
				["s0_dm_lore_honesty_slice"] = WorldSession0IntentBoard.DmLoreHonestySliceId,
				["ux_bullet"] = "UX-1",
				["dials_summary"] = _dials.SummaryLine(),
				["scaffold_id"] = _scaffold.ScaffoldId,
				["scaffold_revision"] = _scaffold.Revision,
				["intent_accepted_count"] = _intents.AcceptedCount,
				["intent_summary"] = _intents.SummaryLine,
				["lore_feed_salt"] = _intents.LoreFeedSalt,
				["lore_fed"] = _intents.LoreFed,
				["s0_off_critical_path"] = true,
			});

		EmitSignal(SignalName.ScaffoldAccepted, _scaffold.ScaffoldId, s.Label);
	}

	private void OnCancel()
	{
		AlphaFactoryLog.Emit("ui.boundary", "Flow_Launch", "WORLD-propose dialogue cancelled");
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
