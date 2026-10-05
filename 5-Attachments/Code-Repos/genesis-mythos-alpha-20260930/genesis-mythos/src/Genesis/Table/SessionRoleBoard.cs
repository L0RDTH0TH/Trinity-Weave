using System;
using Genesis.Core;
using Genesis.Module;
using Godot;

namespace Genesis.Table;

/// <summary>Session roles after Enter — DM + Player seats; one human may run both offline.</summary>
public partial class SessionRoleBoard : CanvasLayer
{
	public event Action<SeatId, string>? ContinueRequested;
	public event Action? BackRequested;

	private ModulePack? _pack;
	private SeatId _activeSeat = SeatId.Player;
	private string _pregenId = "";
	private Label? _seatLabel;
	private Label? _pregenLabel;
	private OptionButton? _pregenPick;
	private Button? _playerSeatBtn;
	private Button? _dmSeatBtn;
	private Button? _continueBtn;
	private ulong _ignoreEnterUntilMsec;

	public SessionRoleBoard()
	{
		Name = "SessionRoleBoard";
		Layer = 41;
		Visible = false;
	}

	public override void _Ready() => Build();

	public void Open(ModulePack pack)
	{
		_pack = pack;
		_pregenId = pack.Pregens.Count > 0 ? pack.Pregens[0].Id : "";
		_activeSeat = SeatId.Player;
		// Same Enter that opened this board must not also Continue.
		_ignoreEnterUntilMsec = Time.GetTicksMsec() + 500;
		RefreshPregenList();
		RefreshSeatUi();
		Visible = true;
		_continueBtn?.GrabFocus();
	}

	public void Close() => Visible = false;

	private void Build()
	{
		var dim = new ColorRect
		{
			Color = new Color(0.04f, 0.05f, 0.08f, 0.92f),
			AnchorRight = 1f,
			AnchorBottom = 1f,
		};
		AddChild(dim);

		var panel = new PanelContainer
		{
			Position = new Vector2(100, 80),
			CustomMinimumSize = new Vector2(680, 420),
		};
		var style = new StyleBoxFlat
		{
			BgColor = new Color(0.08f, 0.09f, 0.12f, 0.98f),
			CornerRadiusTopLeft = 8,
			CornerRadiusTopRight = 8,
			CornerRadiusBottomLeft = 8,
			CornerRadiusBottomRight = 8,
			ContentMarginLeft = 22,
			ContentMarginRight = 22,
			ContentMarginTop = 18,
			ContentMarginBottom = 18,
		};
		panel.AddThemeStyleboxOverride("panel", style);
		AddChild(panel);

		var vbox = new VBoxContainer();
		vbox.AddThemeConstantOverride("separation", 10);
		panel.AddChild(vbox);

		var title = new Label { Text = "Session roles" };
		title.AddThemeFontSizeOverride("font_size", 28);
		title.AddThemeColorOverride("font_color", new Color(0.95f, 0.88f, 0.62f));
		vbox.AddChild(title);

		var blurb = new Label
		{
			Text = "Offline: one human may switch between Player and DM seats. Player seat cannot own the DM table rail.\nAfter Continue: FP explore/intent verbs → PF1 resolve; DM seat shows called checks + relationship/history.",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
			CustomMinimumSize = new Vector2(620, 0),
		};
		blurb.AddThemeFontSizeOverride("font_size", 14);
		blurb.AddThemeColorOverride("font_color", new Color(0.75f, 0.78f, 0.82f));
		vbox.AddChild(blurb);

		_seatLabel = new Label { Text = "Active seat: Player" };
		_seatLabel.AddThemeFontSizeOverride("font_size", 16);
		vbox.AddChild(_seatLabel);

		var seatRow = new HBoxContainer();
		seatRow.AddThemeConstantOverride("separation", 12);
		vbox.AddChild(seatRow);

		_playerSeatBtn = new Button { Text = "Take Player seat", CustomMinimumSize = new Vector2(180, 40) };
		_playerSeatBtn.FocusMode = Control.FocusModeEnum.None;
		_playerSeatBtn.Pressed += () =>
		{
			_activeSeat = SeatId.Player;
			RefreshSeatUi();
		};
		seatRow.AddChild(_playerSeatBtn);

		_dmSeatBtn = new Button { Text = "Take DM seat", CustomMinimumSize = new Vector2(180, 40) };
		_dmSeatBtn.FocusMode = Control.FocusModeEnum.None;
		_dmSeatBtn.Pressed += () =>
		{
			_activeSeat = SeatId.DmAsPlayer;
			RefreshSeatUi();
		};
		seatRow.AddChild(_dmSeatBtn);

		var pregLbl = new Label { Text = "Player pregen (from loaded pack)" };
		pregLbl.AddThemeFontSizeOverride("font_size", 16);
		vbox.AddChild(pregLbl);

		_pregenPick = new OptionButton { CustomMinimumSize = new Vector2(420, 36) };
		_pregenPick.ItemSelected += OnPregenSelected;
		vbox.AddChild(_pregenPick);

		_pregenLabel = new Label
		{
			Text = "",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
			CustomMinimumSize = new Vector2(620, 0),
		};
		_pregenLabel.AddThemeFontSizeOverride("font_size", 13);
		_pregenLabel.AddThemeColorOverride("font_color", new Color(0.8f, 0.82f, 0.86f));
		vbox.AddChild(_pregenLabel);

		var row = new HBoxContainer();
		row.AddThemeConstantOverride("separation", 14);
		vbox.AddChild(row);

		var cont = new Button { Text = "Continue into site", CustomMinimumSize = new Vector2(220, 44) };
		cont.Pressed += () =>
		{
			if (_pack == null || string.IsNullOrEmpty(_pregenId)) return;
			ContinueRequested?.Invoke(_activeSeat, _pregenId);
		};
		row.AddChild(cont);
		_continueBtn = cont;

		var back = new Button { Text = "Back", CustomMinimumSize = new Vector2(100, 44) };
		back.FocusMode = Control.FocusModeEnum.None;
		back.Pressed += () => BackRequested?.Invoke();
		row.AddChild(back);
	}

	public void RequestContinue()
	{
		if (!Visible || _pack == null || string.IsNullOrEmpty(_pregenId)) return;
		ContinueRequested?.Invoke(_activeSeat, _pregenId);
	}

	public override void _Input(InputEvent @event)
	{
		if (!Visible) return;
		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.Enter }
		    or InputEventKey { Pressed: true, Echo: false, Keycode: Key.KpEnter })
		{
			if (Time.GetTicksMsec() < _ignoreEnterUntilMsec) return;
			RequestContinue();
			GetViewport().SetInputAsHandled();
		}
	}

	private void RefreshPregenList()
	{
		_pregenPick?.Clear();
		if (_pack == null) return;
		for (var i = 0; i < _pack.Pregens.Count; i++)
		{
			var p = _pack.Pregens[i];
			_pregenPick?.AddItem($"{p.Name}  HP {p.Hp}/{p.HpMax}  atk +{p.AttackMod}");
			if (p.Id == _pregenId)
				_pregenPick?.Select(i);
		}
		RefreshPregenDetail();
	}

	private void OnPregenSelected(long index)
	{
		if (_pack == null || index < 0 || index >= _pack.Pregens.Count) return;
		_pregenId = _pack.Pregens[(int)index].Id;
		RefreshPregenDetail();
	}

	private void RefreshPregenDetail()
	{
		var p = _pack?.FindPregen(_pregenId);
		if (_pregenLabel == null) return;
		if (p == null)
		{
			_pregenLabel.Text = "";
			return;
		}
		_pregenLabel.Text = $"{p.AncestryLabel} · AC {p.Ac} · dmg {p.Damage}\n{p.SkillsSummary()}";
	}

	private void RefreshSeatUi()
	{
		if (_seatLabel != null)
			_seatLabel.Text = _activeSeat == SeatId.DmAsPlayer
				? "Active seat: DM (table rail allowed)"
				: "Active seat: Player (DM rail refused)";
		if (_playerSeatBtn != null)
			_playerSeatBtn.Disabled = _activeSeat == SeatId.Player;
		if (_dmSeatBtn != null)
			_dmSeatBtn.Disabled = _activeSeat == SeatId.DmAsPlayer;
	}
}
