using System;
using System.Collections.Generic;
using Genesis.Module;
using Godot;

namespace Genesis.Table;

/// <summary>Alpha 0 front door — Host table → pick module → Enter play / Exit.</summary>
public partial class FrontDoorUi : CanvasLayer
{
	public event Action<string>? EnterPlayRequested;
	public event Action? ExitRequested;

	private ItemList? _moduleList;
	private Label? _detail;
	private Button? _enterBtn;
	private readonly List<ModulePackCatalogEntry> _entries = new();
	private string _selectedPackId = ModulePackLoader.DefaultCartridgePackId;

	public FrontDoorUi()
	{
		Name = "FrontDoorUi";
		Layer = 40;
	}

	public override void _Ready()
	{
		Build();
		RefreshCatalog();
	}

	private void Build()
	{
		var dim = new ColorRect
		{
			Color = new Color(0.04f, 0.05f, 0.08f, 0.94f),
			AnchorRight = 1f,
			AnchorBottom = 1f,
		};
		AddChild(dim);

		var panel = new PanelContainer
		{
			Position = new Vector2(80, 60),
			CustomMinimumSize = new Vector2(720, 520),
		};
		var style = new StyleBoxFlat
		{
			BgColor = new Color(0.08f, 0.09f, 0.12f, 0.98f),
			CornerRadiusTopLeft = 8,
			CornerRadiusTopRight = 8,
			CornerRadiusBottomLeft = 8,
			CornerRadiusBottomRight = 8,
			ContentMarginLeft = 24,
			ContentMarginRight = 24,
			ContentMarginTop = 20,
			ContentMarginBottom = 20,
			BorderWidthLeft = 1,
			BorderWidthRight = 1,
			BorderWidthTop = 1,
			BorderWidthBottom = 1,
			BorderColor = new Color(0.45f, 0.38f, 0.22f, 0.7f),
		};
		panel.AddThemeStyleboxOverride("panel", style);
		AddChild(panel);

		var vbox = new VBoxContainer();
		vbox.AddThemeConstantOverride("separation", 12);
		panel.AddChild(vbox);

		var brand = new Label { Text = "Genesis Mythos — Table" };
		brand.AddThemeFontSizeOverride("font_size", 32);
		brand.AddThemeColorOverride("font_color", new Color(0.95f, 0.88f, 0.62f));
		vbox.AddChild(brand);

		var tag = new Label
		{
			Text = "Offline Alpha 0 · Host one machine · Modules are cartridges (not the product name)\nInvestor path: Host table → pick pack → Enter play → seats → explore/intent → PF1 resolve",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
			CustomMinimumSize = new Vector2(660, 0),
		};
		tag.AddThemeFontSizeOverride("font_size", 14);
		tag.AddThemeColorOverride("font_color", new Color(0.7f, 0.74f, 0.78f));
		vbox.AddChild(tag);

		var hostLbl = new Label { Text = "1) Host table" };
		hostLbl.AddThemeFontSizeOverride("font_size", 18);
		hostLbl.AddThemeColorOverride("font_color", new Color(0.85f, 0.9f, 0.95f));
		vbox.AddChild(hostLbl);

		var hostStatus = new Label { Text = "Local host ready (no LAN)." };
		hostStatus.AddThemeFontSizeOverride("font_size", 14);
		hostStatus.AddThemeColorOverride("font_color", new Color(0.55f, 0.8f, 0.6f));
		vbox.AddChild(hostStatus);

		var pickLbl = new Label { Text = "2) Pick module cartridge" };
		pickLbl.AddThemeFontSizeOverride("font_size", 18);
		vbox.AddChild(pickLbl);

		_moduleList = new ItemList
		{
			CustomMinimumSize = new Vector2(660, 140),
			AllowReselect = true,
		};
		_moduleList.ItemSelected += OnModuleSelected;
		vbox.AddChild(_moduleList);

		_detail = new Label
		{
			Text = "",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
			CustomMinimumSize = new Vector2(660, 70),
		};
		_detail.AddThemeFontSizeOverride("font_size", 13);
		_detail.AddThemeColorOverride("font_color", new Color(0.78f, 0.8f, 0.84f));
		vbox.AddChild(_detail);

		var honesty = new Label
		{
			Text = "PDF-derived structured cartridge preferred — NOT campaign ship. No Paizo prose dump. No LAN. claim_class staging.",
			AutowrapMode = TextServer.AutowrapMode.WordSmart,
			CustomMinimumSize = new Vector2(660, 0),
		};
		honesty.AddThemeFontSizeOverride("font_size", 12);
		honesty.AddThemeColorOverride("font_color", new Color(0.65f, 0.68f, 0.55f));
		vbox.AddChild(honesty);

		var row = new HBoxContainer();
		row.AddThemeConstantOverride("separation", 16);
		vbox.AddChild(row);

		_enterBtn = new Button
		{
			Text = "3) Enter play",
			CustomMinimumSize = new Vector2(200, 44),
		};
		_enterBtn.Pressed += () =>
		{
			if (!string.IsNullOrEmpty(_selectedPackId))
				EnterPlayRequested?.Invoke(_selectedPackId);
		};
		row.AddChild(_enterBtn);

		var exitBtn = new Button
		{
			Text = "Exit",
			CustomMinimumSize = new Vector2(120, 44),
		};
		exitBtn.Pressed += () => ExitRequested?.Invoke();
		row.AddChild(exitBtn);
	}

	public void RequestEnterSelected()
	{
		if (!Visible) return;
		if (!string.IsNullOrEmpty(_selectedPackId) && _enterBtn is { Disabled: false })
			EnterPlayRequested?.Invoke(_selectedPackId);
	}

	public override void _Input(InputEvent @event)
	{
		if (!Visible) return;
		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.Enter }
		    or InputEventKey { Pressed: true, Echo: false, Keycode: Key.KpEnter })
		{
			RequestEnterSelected();
			GetViewport().SetInputAsHandled();
		}
	}

	public void RefreshCatalog()
	{
		_entries.Clear();
		_moduleList?.Clear();
		foreach (var e in ModulePackLoader.ListAvailablePacks())
		{
			_entries.Add(e);
			_moduleList?.AddItem($"{e.Title}  [{e.PackId}]");
		}

		if (_entries.Count == 0)
		{
			if (_detail != null)
				_detail.Text = "No packs found under content/packs/. Expected we_be_goblins_free_struct.";
			if (_enterBtn != null) _enterBtn.Disabled = true;
			return;
		}

		var idx = 0;
		for (var i = 0; i < _entries.Count; i++)
		{
			if (_entries[i].PackId == ModulePackLoader.DefaultCartridgePackId)
			{
				idx = i;
				break;
			}
		}
		_moduleList?.Select(idx);
		OnModuleSelected((long)idx);
		if (_enterBtn != null) _enterBtn.Disabled = false;
	}

	private void OnModuleSelected(long index)
	{
		if (index < 0 || index >= _entries.Count) return;
		var e = _entries[(int)index];
		_selectedPackId = e.PackId;
		if (_detail != null)
			_detail.Text = string.IsNullOrEmpty(e.Subtitle)
				? $"Pack id: {e.PackId}\nPath: {e.PackRootResPath}"
				: $"{e.Subtitle}\nPack id: {e.PackId} · {e.PackRootResPath}";
	}

	public void ShowDoor()
	{
		Visible = true;
		RefreshCatalog();
	}

	public void HideDoor() => Visible = false;
}
