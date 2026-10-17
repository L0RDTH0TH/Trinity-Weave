using System;
using System.Collections.Generic;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Session 0 collaborative intent — Microscope-informed seed that enters
/// <c>proposed → accepted</c> (or rejected). Not GEN-* fill; not world authorship by players.
/// DM owns world authority; players may seed intents.
/// </summary>
public sealed class WorldSession0Intent
{
	public enum Disposition
	{
		Proposed = 0,
		Accepted = 1,
		Rejected = 2,
	}

	public enum AuthorSeat
	{
		Player = 0,
		Dm = 1,
		Shared = 2,
	}

	public string IntentId { get; }
	public string Text { get; }
	public AuthorSeat Seat { get; }
	public Disposition Status { get; }
	public int Ordinal { get; }

	public bool CanAccept => Status == Disposition.Proposed;
	public bool IsAccepted => Status == Disposition.Accepted;

	public string SeatId => Seat switch
	{
		AuthorSeat.Player => "player",
		AuthorSeat.Dm => "dm",
		AuthorSeat.Shared => "shared",
		_ => "shared",
	};

	public string StatusId => Status.ToString().ToLowerInvariant();

	private WorldSession0Intent(
		string intentId,
		string text,
		AuthorSeat seat,
		Disposition status,
		int ordinal)
	{
		IntentId = intentId;
		Text = text;
		Seat = seat;
		Status = status;
		Ordinal = ordinal;
	}

	public static WorldSession0Intent CreateProposed(
		string intentId,
		string text,
		AuthorSeat seat,
		int ordinal) =>
		new(intentId, text.Trim(), seat, Disposition.Proposed, ordinal);

	/// <summary>Optional lore capture — filled lines land as accepted seeds (never required).</summary>
	public static WorldSession0Intent CreateAccepted(
		string intentId,
		string text,
		AuthorSeat seat,
		int ordinal) =>
		new(intentId, text.Trim(), seat, Disposition.Accepted, ordinal);

	public WorldSession0Intent AsAccepted() =>
		new(IntentId, Text, Seat, Disposition.Accepted, Ordinal);

	public WorldSession0Intent AsRejected() =>
		new(IntentId, Text, Seat, Disposition.Rejected, Ordinal);

	public string CardLine() =>
		$"[{SeatId.ToUpperInvariant()}] {StatusId} · {Text}";

	public Dictionary<string, object> ToLogFields() => new()
	{
		["intent_id"] = IntentId,
		["intent_text"] = Text,
		["intent_seat"] = SeatId,
		["intent_status"] = StatusId,
		["intent_ordinal"] = Ordinal,
	};
}
