using System.Collections.Generic;
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
/// Alpha 0 playable table: pack stages → explore/intent → PF1 resolve → seat-routed results/DM context.
/// claim_class staging — not ask_success until operator attest.
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
	private Node3D? _playWorld;
	private Node3D? _siteRoot;

	private int _stageIndex;
	private readonly HashSet<string> _completedIntentIds = new();
	private readonly HashSet<string> _exploredStageIds = new();
	private IntentBeat? _activeSkirmishIntent;

	private Label? _hudTitle;
	private Label? _hudBody;
	private Label? _hudSheet;
	private Label? _hudResult;
	private Label? _honesty;
	private Label? _controls;
	private Label? _toast;
	private ColorRect? _toastBg;
	private Label? _seatBadge;
	private Label? _fpPanel;
	private Label? _dmContext;
	private Label? _stageLabel;
	private readonly List<string> _calledCheckLog = new();
	private readonly List<string> _sessionHistory = new();
	private VBoxContainer? _intentColumn;
	private Button? _attackBtn;
	private Button? _advanceBtn;
	private Button? _seatPlayerBtn;
	private Button? _seatDmBtn;
	private Button? _dmRailBtn;
	private Button? _backDoorBtn;
	private CanvasLayer? _hud;
	private PanelContainer? _fpChrome;
	private PanelContainer? _dmChrome;
	private PanelContainer? _resultChrome;

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
		_activeSeat = initialSeat;
		_stageIndex = 0;
		_completedIntentIds.Clear();
		_exploredStageIds.Clear();
		_calledCheckLog.Clear();
		_sessionHistory.Clear();
		_activeSkirmishIntent = null;
		_skirmishStarted = false;
		_skirmishOver = false;
		_rollSeed = (ulong)Time.GetTicksMsec();

		var stage = pack.StageAt(0);
		var siteId = stage != null && !string.IsNullOrEmpty(stage.SiteId)
			? stage.SiteId
			: pack.DefaultSiteId;
		_site = pack.FindSite(siteId) ?? pack.Sites[0];
		_enemy = null;

		ClearChildren();
		BuildHud();
		var err = MountTable();
		if (err != Error.Ok) return err;

		RefreshHud();
		RefreshIntentButtons();
		RefreshDmContext();
		RefreshSeatPanels();
		ApplySeatCamera(showRefuseToast: false);
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
		_playWorld = null;
		_siteRoot = null;
		_intentColumn = null;
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
		_playWorld = playRegion.PlayWorld;

		_siteRoot = ModuleSiteBuilder.Build(_playWorld, _site);

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
			$"pack_id={_pack.PackId};pregens={_pack.Pregens.Count};sites={_pack.Sites.Count};stages={_pack.Stages.Count}");

		return Error.Ok;
	}

	private void TravelToStage(int index)
	{
		if (_pack == null || _playWorld == null) return;
		var stage = _pack.StageAt(index);
		if (stage == null) return;

		if (stage.RequireIntentBeforeAdvance && index > _stageIndex)
		{
			var prior = _pack.StageAt(index - 1);
			if (prior != null && !StageHasCompletedIntent(prior))
			{
				ShowToast("Complete at least one intent on this stage before advancing");
				return;
			}
		}

		_stageIndex = index;
		_site = _pack.FindSite(stage.SiteId) ?? _site;
		_activeSkirmishIntent = null;
		_skirmishStarted = false;
		_skirmishOver = false;
		_enemy = null;

		if (_siteRoot != null && GodotObject.IsInstanceValid(_siteRoot))
			_siteRoot.QueueFree();
		_siteRoot = null;
		if (_site != null)
			_siteRoot = ModuleSiteBuilder.Build(_playWorld, _site);

		if (_cams != null && _site != null)
		{
			_cams.SetSpawnOrigin(_site.SpawnEye);
			_cams.SetDmOrigin(_site.DmEye);
			_cams.ApplySpawnOriginsToMountedRigs();
			ApplySeatCamera(showRefuseToast: false);
		}

		_sessionHistory.Add($"[travel] → {stage.Title} ({stage.SiteId})");
		SetResult($"Arrived: {stage.Title}\n{stage.ExploreBlurb}");
		RefreshHud();
		RefreshIntentButtons();
		RefreshDmContext();
		RefreshSeatPanels();
		CallDeferred(nameof(ReleaseUiFocusForPlay));
	}

	private bool StageHasCompletedIntent(AdventureStage stage)
	{
		foreach (var intent in stage.Intents)
		{
			if (_completedIntentIds.Contains(intent.Id)) return true;
			if (intent.Kind == "explore" && _exploredStageIds.Contains(stage.Id)) return true;
		}
		return false;
	}

	private void BuildHud()
	{
		_hud = new CanvasLayer { Name = "TableHud", Layer = 25 };
		AddChild(_hud);

		_fpChrome = MakePanel(new Vector2(20, 16), new Vector2(540, 150), new Color(0.05f, 0.07f, 0.10f, 0.82f));
		_hud.AddChild(_fpChrome);
		var fpBox = new VBoxContainer { MouseFilter = Control.MouseFilterEnum.Ignore };
		fpBox.AddThemeConstantOverride("separation", 4);
		_fpChrome.AddChild(fpBox);

		_hudTitle = MakeLabel("Table", 22, new Color(0.95f, 0.88f, 0.62f));
		fpBox.AddChild(_hudTitle);
		_seatBadge = MakeLabel("", 14, new Color(0.85f, 0.82f, 0.55f));
		fpBox.AddChild(_seatBadge);
		_stageLabel = MakeLabel("", 13, new Color(0.7f, 0.85f, 0.95f));
		fpBox.AddChild(_stageLabel);
		_hudBody = MakeLabel("", 13, new Color(0.88f, 0.90f, 0.94f), wrapWidth: 500);
		fpBox.AddChild(_hudBody);

		_fpPanel = MakeLabel("", 13, new Color(0.72f, 0.9f, 0.78f), wrapWidth: 500);
		_fpPanel.Position = new Vector2(24, 178);
		_hud.AddChild(_fpPanel);

		_hudSheet = MakeLabel("", 13, new Color(0.75f, 0.9f, 0.8f));
		_hudSheet.Position = new Vector2(24, 250);
		_hud.AddChild(_hudSheet);

		_honesty = MakeLabel(
			"PDF-derived structured pack — NOT campaign ship / no Paizo prose. No LAN. claim_class staging.",
			12, new Color(0.62f, 0.66f, 0.55f), wrapWidth: 700);
		_honesty.Position = new Vector2(24, 278);
		_hud.AddChild(_honesty);

		_dmChrome = MakePanel(new Vector2(720, 16), new Vector2(460, 320), new Color(0.06f, 0.08f, 0.12f, 0.88f));
		_hud.AddChild(_dmChrome);
		_dmContext = MakeLabel("", 13, new Color(0.72f, 0.86f, 0.95f), wrapWidth: 430);
		_dmChrome.AddChild(_dmContext);
		_dmChrome.Visible = false;

		_resultChrome = MakePanel(new Vector2(20, 310), new Vector2(680, 110), new Color(0.07f, 0.07f, 0.05f, 0.85f));
		_hud.AddChild(_resultChrome);
		_hudResult = MakeLabel("", 15, new Color(0.95f, 0.92f, 0.75f), wrapWidth: 650);
		_resultChrome.AddChild(_hudResult);

		_toastBg = new ColorRect
		{
			Color = new Color(0.5f, 0.06f, 0.06f, 0.9f),
			Position = new Vector2(24, 430),
			Size = new Vector2(680, 44),
			Visible = false,
		};
		_hud.AddChild(_toastBg);
		_toast = MakeLabel("", 18, new Color(1f, 0.5f, 0.5f));
		_toast.Position = new Vector2(36, 438);
		_toast.Visible = false;
		_hud.AddChild(_toast);

		_intentColumn = new VBoxContainer
		{
			Position = new Vector2(20, 485),
			CustomMinimumSize = new Vector2(900, 0),
		};
		_intentColumn.AddThemeConstantOverride("separation", 8);
		_hud.AddChild(_intentColumn);

		var seatRow = new HBoxContainer();
		seatRow.AddThemeConstantOverride("separation", 10);
		_intentColumn.AddChild(seatRow);

		_seatPlayerBtn = new Button { Text = "Seat: Player", CustomMinimumSize = new Vector2(130, 34), FocusMode = Control.FocusModeEnum.None };
		_seatPlayerBtn.Pressed += () => SwitchSeat(SeatId.Player);
		seatRow.AddChild(_seatPlayerBtn);

		_seatDmBtn = new Button { Text = "Seat: DM", CustomMinimumSize = new Vector2(110, 34), FocusMode = Control.FocusModeEnum.None };
		_seatDmBtn.Pressed += () => SwitchSeat(SeatId.DmAsPlayer);
		seatRow.AddChild(_seatDmBtn);

		_dmRailBtn = new Button { Text = "DM cam", CustomMinimumSize = new Vector2(110, 34), FocusMode = Control.FocusModeEnum.None };
		_dmRailBtn.Pressed += ToggleDmRail;
		seatRow.AddChild(_dmRailBtn);

		_attackBtn = new Button { Text = "Attack", CustomMinimumSize = new Vector2(100, 34), Disabled = true, FocusMode = Control.FocusModeEnum.None };
		_attackBtn.Pressed += ResolveAttack;
		seatRow.AddChild(_attackBtn);

		_advanceBtn = new Button { Text = "Next stage →", CustomMinimumSize = new Vector2(140, 34), FocusMode = Control.FocusModeEnum.None };
		_advanceBtn.Pressed += AdvanceStage;
		seatRow.AddChild(_advanceBtn);

		_backDoorBtn = new Button { Text = "Front door", CustomMinimumSize = new Vector2(120, 34), FocusMode = Control.FocusModeEnum.None };
		_backDoorBtn.Pressed += () =>
		{
			_cams?.ReleaseMouseCapture();
			Input.MouseMode = Input.MouseModeEnum.Visible;
			ReturnToFrontDoor?.Invoke();
		};
		seatRow.AddChild(_backDoorBtn);

		var intentHeader = MakeLabel("Intents (GUI verbs — not hotkey-demo Success)", 13, new Color(0.8f, 0.82f, 0.7f));
		_intentColumn.AddChild(intentHeader);

		_controls = MakeLabel(
			"WASD move · Mouse look · Esc free mouse · click recapture · Tab DM seat/cam · N next stage\n" +
			"Walk+look caveat (Linux Wayland): simultaneous WASD+mouse may be motion-starved — not a CharacterBody3D defect.",
			12, new Color(0.72f, 0.75f, 0.8f), wrapWidth: 900);
		_controls.Position = new Vector2(24, 680);
		_hud.AddChild(_controls);
	}

	private static PanelContainer MakePanel(Vector2 pos, Vector2 minSize, Color bg)
	{
		var panel = new PanelContainer
		{
			Position = pos,
			CustomMinimumSize = minSize,
			MouseFilter = Control.MouseFilterEnum.Ignore,
		};
		var style = new StyleBoxFlat
		{
			BgColor = bg,
			CornerRadiusTopLeft = 6,
			CornerRadiusTopRight = 6,
			CornerRadiusBottomLeft = 6,
			CornerRadiusBottomRight = 6,
			ContentMarginLeft = 12,
			ContentMarginRight = 12,
			ContentMarginTop = 8,
			ContentMarginBottom = 8,
		};
		panel.AddThemeStyleboxOverride("panel", style);
		return panel;
	}

	private static Label MakeLabel(string text, int size, Color color, float wrapWidth = 0f)
	{
		var label = new Label
		{
			Text = text,
			MouseFilter = Control.MouseFilterEnum.Ignore,
		};
		if (wrapWidth > 0f)
		{
			label.AutowrapMode = TextServer.AutowrapMode.WordSmart;
			label.CustomMinimumSize = new Vector2(wrapWidth, 0);
		}
		label.AddThemeFontSizeOverride("font_size", size);
		label.AddThemeColorOverride("font_color", color);
		return label;
	}

	private void RefreshIntentButtons()
	{
		if (_intentColumn == null || _pack == null) return;

		// Keep seat row (index 0) + header (index 1); free dynamic intent rows after.
		while (_intentColumn.GetChildCount() > 2)
		{
			var last = _intentColumn.GetChild(_intentColumn.GetChildCount() - 1);
			_intentColumn.RemoveChild(last);
			last.QueueFree();
		}

		var stage = _pack.StageAt(_stageIndex);
		if (stage == null) return;

		var row = new HBoxContainer();
		row.AddThemeConstantOverride("separation", 8);
		_intentColumn.AddChild(row);

		foreach (var intent in stage.Intents)
		{
			var done = _completedIntentIds.Contains(intent.Id)
			           || (intent.Kind == "explore" && _exploredStageIds.Contains(stage.Id));
			var label = done ? $"✓ {intent.Verb}: {intent.Title}" : $"{intent.Verb}: {intent.Title}";
			var btn = new Button
			{
				Text = label,
				CustomMinimumSize = new Vector2(200, 36),
				Disabled = done && intent.Kind != "skirmish",
				FocusMode = Control.FocusModeEnum.None,
			};
			if (intent.Kind == "skirmish" && _skirmishStarted && !_skirmishOver)
				btn.Disabled = true;
			var captured = intent;
			btn.Pressed += () => RunIntent(captured);
			row.AddChild(btn);
		}

		if (_pack.Stages.Count > 1)
		{
			var travel = new HBoxContainer();
			travel.AddThemeConstantOverride("separation", 8);
			_intentColumn.AddChild(travel);
			for (var i = 0; i < _pack.Stages.Count; i++)
			{
				var s = _pack.Stages[i];
				var idx = i;
				var tbtn = new Button
				{
					Text = i == _stageIndex ? $"● {s.Title}" : s.Title,
					CustomMinimumSize = new Vector2(220, 30),
					Disabled = i == _stageIndex,
					FocusMode = Control.FocusModeEnum.None,
				};
				tbtn.Pressed += () => TravelToStage(idx);
				travel.AddChild(tbtn);
			}
		}
	}

	private void AdvanceStage()
	{
		if (_pack == null) return;
		if (_stageIndex + 1 >= _pack.Stages.Count)
		{
			SetResult("End of structured cartridge stages — return Front door or revisit sites via stage buttons.");
			return;
		}
		TravelToStage(_stageIndex + 1);
	}

	private void RunIntent(IntentBeat intent)
	{
		if (_pack == null || _pc == null) return;
		if (_activeSeat != SeatId.Player)
		{
			ShowToast("Unauthorized — intents are Player seat actions (DM watches via context panel)");
			return;
		}

		switch (intent.Kind)
		{
			case "explore":
				RunExplore(intent);
				break;
			case "skirmish":
				StartSkirmishFromIntent(intent);
				break;
			default:
				RunSkillIntent(intent);
				break;
		}
	}

	private void RunExplore(IntentBeat intent)
	{
		var stage = _pack?.StageAt(_stageIndex);
		if (stage == null) return;
		_exploredStageIds.Add(stage.Id);
		_completedIntentIds.Add(intent.Id);
		var text =
			$"{intent.Title}\n{intent.Blurb}\n\nStage context:\n{stage.ExploreBlurb}";
		SetResult(text);
		_sessionHistory.Add($"[explore] {intent.Title}");
		_calledCheckLog.Add($"[explore] {intent.Title} (no roll; caller=Player)");
		RefreshDmContext();
		RefreshHud();
		RefreshIntentButtons();
		RefreshSeatPanels();
	}

	private void RunSkillIntent(IntentBeat intent)
	{
		if (_rules == null || _pc == null) return;
		var mod = _pc.SkillModOrDefault(intent.SkillId, 0);
		_rollSeed++;
		var result = _rules.Evaluate(new CheckRequest
		{
			Mode = "check",
			Roll = "1d20",
			Modifier = mod,
			Dc = intent.Dc,
			RulesSubSeed = _rollSeed,
		});
		var d20 = result.Audit?.Rolls.Count > 0 ? (int)result.Audit.Rolls[0].AsInt32() : result.Total - mod;
		var outcome = result.Passed ? "SUCCESS" : "FAILURE";
		var line =
			$"{intent.Verb}: {intent.Title}\n" +
			$"d20 ({d20}) + {intent.SkillFallbackLabel} ({mod:+#;-#;0}) = {result.Total} vs DC {intent.Dc} → {outcome}\n" +
			$"{intent.Blurb}\n(pathfinder_pf1 via rules plugin host)";
		SetResult(line);
		_calledCheckLog.Add(
			$"[called] {intent.SkillFallbackLabel} total={result.Total} DC={intent.Dc} → {outcome} (caller=Player · {intent.Id})");
		_sessionHistory.Add($"[check] {intent.Title} → {outcome}");
		_completedIntentIds.Add(intent.Id);
		RefreshDmContext();
		RefreshHud();
		RefreshIntentButtons();
		RefreshSeatPanels();
	}

	private void StartSkirmishFromIntent(IntentBeat intent)
	{
		if (_pack == null || _pc == null || _rules == null) return;
		if (intent.Enemy == null)
		{
			ShowToast("Skirmish intent missing enemy def");
			return;
		}

		_activeSkirmishIntent = intent;
		_enemy = CloneEnemy(intent.Enemy);
		_rollSeed++;
		var pcInit = _rules.Roll(DiceExpression.Parse("1d20"), RuleContextFrame.FromRulesSeed(_rollSeed)).Total;
		_rollSeed++;
		var enInitAudit = _rules.Roll(DiceExpression.Parse($"1d20+{_enemy.InitiativeMod}"),
			RuleContextFrame.FromRulesSeed(_rollSeed));
		_playerWinsInit = pcInit >= enInitAudit.Total;
		_skirmishStarted = true;
		_skirmishOver = false;
		SetResult(
			$"{intent.Title}\n" +
			$"Initiative — {_pc.Name}: d20={pcInit}  |  {_enemy.Name}: {enInitAudit.Total} " +
			$"(d20+{_enemy.InitiativeMod})\n" +
			$"{(_playerWinsInit ? _pc.Name : _enemy.Name)} acts first. Press Attack.");
		_calledCheckLog.Add($"[called] Initiative scrap vs {_enemy.Name} (caller=Player · {intent.Id})");
		_sessionHistory.Add($"[skirmish] {intent.Title} started");
		RefreshHud();
		RefreshIntentButtons();
		RefreshDmContext();
		RefreshSeatPanels();
	}

	private void RefreshHud()
	{
		if (_pack == null || _pc == null || _site == null) return;
		var stage = _pack.StageAt(_stageIndex);
		if (_hudTitle != null)
			_hudTitle.Text = $"{_pack.Title}";
		if (_stageLabel != null)
			_stageLabel.Text = stage != null
				? $"Stage {_stageIndex + 1}/{_pack.Stages.Count}: {stage.Title} · {_site.Name}"
				: _site.Name;
		if (_hudBody != null)
			_hudBody.Text = stage != null
				? $"{_site.Blurb}\n{stage.ExploreBlurb}"
				: $"{_site.Blurb}\nPack id: {_pack.PackId} · rules: {_pack.RulesetBind}";
		if (_hudSheet != null)
			_hudSheet.Text =
				$"{_pc.Name}  HP {_pc.Hp}/{_pc.HpMax}  AC {_pc.Ac}  atk +{_pc.AttackMod}  dmg {_pc.Damage}  ·  {_pc.SkillsSummary()}";
		if (_seatBadge != null)
			_seatBadge.Text = _activeSeat == SeatId.DmAsPlayer
				? "Active seat: DM — context panel shows called checks + relationships"
				: "Active seat: Player — FP explore/intent; results panel below";
		if (_attackBtn != null)
			_attackBtn.Disabled = !_skirmishStarted || _skirmishOver || _activeSeat != SeatId.Player;
		if (_advanceBtn != null)
			_advanceBtn.Disabled = _pack.Stages.Count == 0 || _stageIndex >= _pack.Stages.Count - 1;
	}

	private void RefreshSeatPanels()
	{
		if (_fpPanel != null)
		{
			var stage = _pack?.StageAt(_stageIndex);
			_fpPanel.Text = _activeSeat == SeatId.Player
				? $"FP PANEL · Intents available: {stage?.Intents.Count ?? 0} · completed this run: {_completedIntentIds.Count}"
				: "FP PANEL (inactive while DM seat) — switch Seat: Player to act.";
		}
		if (_fpChrome != null)
			_fpChrome.Modulate = _activeSeat == SeatId.Player
				? Colors.White
				: new Color(0.75f, 0.75f, 0.8f, 0.85f);
		if (_dmChrome != null)
			_dmChrome.Visible = _activeSeat == SeatId.DmAsPlayer;
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
		RefreshDmContext();
		RefreshSeatPanels();
		ApplySeatCamera(showRefuseToast: false);
		SetResult(seat == SeatId.DmAsPlayer
			? "Switched to DM seat — called checks + relationship/history for RP (right panel)."
			: "Switched to Player seat — FP control + intent verbs. DM rail will refuse.");
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
		log.AppendLine(_activeSkirmishIntent?.Title ?? _pack.Skirmish.Title);

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
			if (_activeSkirmishIntent != null)
				_completedIntentIds.Add(_activeSkirmishIntent.Id);
		}
		else if (_pc.Hp <= 0)
		{
			_pc.Hp = 0;
			_skirmishOver = true;
			log.AppendLine($"{_pc.Name} is down — scrap over (placeholder).");
			if (_activeSkirmishIntent != null)
				_completedIntentIds.Add(_activeSkirmishIntent.Id);
		}
		else
		{
			log.AppendLine("Press Attack again for another exchange.");
		}

		SetResult(log.ToString().TrimEnd());
		_calledCheckLog.Add($"[called] Attack exchange → PC HP {_pc.Hp}/{_pc.HpMax} | enemy HP {_enemy.Hp}/{_enemy.HpMax}");
		RefreshHud();
		RefreshIntentButtons();
		RefreshDmContext();
		RefreshSeatPanels();
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

	private void RefreshDmContext()
	{
		if (_dmContext == null) return;
		var dmSeat = _activeSeat == SeatId.DmAsPlayer;
		if (_dmChrome != null) _dmChrome.Visible = dmSeat;
		if (!dmSeat || _pack == null)
		{
			_dmContext.Text = "";
			return;
		}
		var sb = new System.Text.StringBuilder();
		sb.AppendLine("DM CONTEXT (seat-routed)");
		sb.AppendLine("— Called checks / explores —");
		if (_calledCheckLog.Count == 0)
			sb.AppendLine("(none yet — Player seat runs intents)");
		else
			foreach (var c in _calledCheckLog)
				sb.AppendLine(c);
		sb.AppendLine();
		sb.AppendLine("— Relationship / history (RP feed) —");
		if (_pack.Relationships.Count == 0)
			sb.AppendLine("(pack has no relationships[])");
		else
			foreach (var r in _pack.Relationships)
			{
				sb.AppendLine($"{r.Label} [{r.Disposition}]");
				sb.AppendLine($"  hist: {r.History}");
				if (r.RpHooks.Count > 0)
					sb.AppendLine($"  hooks: {string.Join("; ", r.RpHooks)}");
			}
		if (_sessionHistory.Count > 0)
		{
			sb.AppendLine();
			sb.AppendLine("— Session trail —");
			var start = System.Math.Max(0, _sessionHistory.Count - 8);
			for (var i = start; i < _sessionHistory.Count; i++)
				sb.AppendLine(_sessionHistory[i]);
		}
		_dmContext.Text = sb.ToString();
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
			_cams?.ReleaseMouseCapture();
			Input.MouseMode = Input.MouseModeEnum.Visible;
			GetViewport().SetInputAsHandled();
			return;
		}

		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.Tab })
		{
			if (_cams == null) return;
			if (_activeSeat == SeatId.Player)
				SwitchSeat(SeatId.DmAsPlayer);
			else
				ToggleDmRail();
			GetViewport().SetInputAsHandled();
			return;
		}

		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.N })
		{
			AdvanceStage();
			GetViewport().SetInputAsHandled();
		}
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		// Hotkeys remain available as convenience — Success bar is GUI intents + seats, not hotkeys alone.
		if (!Visible) return;
		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.B })
		{
			ResolveAttack();
			GetViewport().SetInputAsHandled();
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
		Skills = new List<SkillMod>(p.Skills),
	};
}
