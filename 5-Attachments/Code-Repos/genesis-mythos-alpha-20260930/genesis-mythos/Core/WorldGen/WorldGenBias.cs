namespace Genesis.Core.WorldGen;

/// <summary>
/// Default world-create gen bias (WORLD-new). Not a campaign ToneProfile bind —
/// campaigns may later inherit or override per PMG.
/// </summary>
public enum WorldGenBias
{
	High = 0,
	Medium = 1,
	Low = 2,
	Grimdark = 3,
}
