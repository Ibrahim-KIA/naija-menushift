import { NextResponse } from "next/server";
import { DEFAULT_BRIEF, exploreLocal, type Brief } from "@/lib/engine";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * POST /api/explore
 *
 * Tonight: runs the built-in TypeScript engine (lib/engine.ts), a mirror of
 * the Python prototype, and returns engineMode: "local".
 *
 * Tomorrow on AWS: set MENUSHIFT_ENGINE_URL to the base URL of the hosted
 * Python engine (API Gateway / Lambda / ECS / App Runner). This route then
 * proxies the brief to POST {MENUSHIFT_ENGINE_URL}/explore and returns the
 * upstream response untouched. The UI does not change.
 */
export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Request body must be JSON" }, { status: 400 });
  }

  const brief: Brief = { ...DEFAULT_BRIEF, ...(body as Partial<Brief>) };

  const upstream = process.env.MENUSHIFT_ENGINE_URL?.trim();
  if (upstream) {
    try {
      const res = await fetch(`${upstream.replace(/\/$/, "")}/explore`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(brief),
      });
      const text = await res.text();
      return new NextResponse(text, {
        status: res.status,
        headers: {
          "content-type": res.headers.get("content-type") ?? "application/json",
        },
      });
    } catch {
      return NextResponse.json(
        { error: "AWS engine is configured but unreachable" },
        { status: 502 },
      );
    }
  }

  try {
    const result = exploreLocal(brief);
    return NextResponse.json(result);
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Invalid brief" },
      { status: 400 },
    );
  }
}
