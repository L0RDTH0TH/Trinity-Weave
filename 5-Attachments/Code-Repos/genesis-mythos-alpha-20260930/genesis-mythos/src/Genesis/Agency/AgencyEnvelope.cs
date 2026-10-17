using Genesis.Core;
using Genesis.Exemplar;
using Godot;

namespace Genesis.Agency;

public interface IAgencyEnvelope
{
	Error Assert(SeatContext seat);
	Error Release(StringName pilotId);
}

/// <summary>FP ≠ DM rail — wrong seat fails Unauthorized.</summary>
public sealed class AgencyEnvelope : IAgencyEnvelope
{
	private StringName? _activePilot;
	private SeatId? _boundSeat;
	private ReceiptLedger? _ledger;

	public void BindLedger(ReceiptLedger ledger) => _ledger = ledger;

	public Error Assert(SeatContext seat)
	{
		// Conflating FP player with DM world authorship → Unauthorized.
		if (seat.Id == SeatId.Player && _boundSeat == SeatId.DmAsPlayer)
		{
			_ledger?.Record("R.agency.envelope", "placeholder_ok", "wrong_seat=Unauthorized",
				"agency.envelope", "slot.agency.envelope");
			return Error.Unauthorized;
		}
		if (seat.Id == SeatId.DmAsPlayer && _boundSeat == SeatId.Player)
		{
			_ledger?.Record("R.agency.envelope", "placeholder_ok", "wrong_seat=Unauthorized",
				"agency.envelope", "slot.agency.envelope");
			return Error.Unauthorized;
		}
		_boundSeat = seat.Id;
		_activePilot ??= new StringName("pilot_default");
		_ledger?.Record("R.agency.envelope", "placeholder_ok", "wrong_seat=Unauthorized",
			"agency.envelope", "slot.agency.envelope");
		return Error.Ok;
	}

	public Error Release(StringName pilotId)
	{
		if (_activePilot == null || _activePilot != pilotId)
			return Error.DoesNotExist;
		_activePilot = null;
		_boundSeat = null;
		return Error.Ok;
	}

	/// <summary>Proof probe: bind player then assert DM conflation refuses.</summary>
	public Error ProbeWrongSeatRefuse()
	{
		var ok = Assert(SeatContext.Player);
		if (ok != Error.Ok) return ok;
		var refuse = Assert(SeatContext.DmAsPlayer);
		return refuse == Error.Unauthorized ? Error.Ok : Error.Bug;
	}
}
