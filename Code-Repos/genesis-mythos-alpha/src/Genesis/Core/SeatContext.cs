namespace Genesis.Core;

using Godot;

/// <summary>Seat identity for authority checks. Wrong seat → Error.Unauthorized.</summary>
public enum SeatId
{
	SessionCompose,
	Player,
	DmAsPlayer,
	Simulation,
	Presentation,
	SharedTable,
}

public readonly struct SeatContext
{
	public SeatId Id { get; }

	public SeatContext(SeatId id) => Id = id;

	public static SeatContext SessionCompose => new(SeatId.SessionCompose);
	public static SeatContext Player => new(SeatId.Player);
	public static SeatContext DmAsPlayer => new(SeatId.DmAsPlayer);
	public static SeatContext Simulation => new(SeatId.Simulation);
	public static SeatContext Presentation => new(SeatId.Presentation);
	public static SeatContext SharedTable => new(SeatId.SharedTable);

	public bool AllowsSessionCompose() => Id == SeatId.SessionCompose;

	public Error Guard(SeatId required) =>
		Id == required ? Error.Ok : Error.Unauthorized;

	public Error GuardAny(params SeatId[] allowed)
	{
		foreach (var a in allowed)
		{
			if (Id == a) return Error.Ok;
		}
		return Error.Unauthorized;
	}
}
