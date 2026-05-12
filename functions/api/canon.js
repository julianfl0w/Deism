export async function onRequestGet({ request }) {
  const canonUrl = new URL("/canon.json", request.url);
  const response = await fetch(canonUrl);

  if (!response.ok) {
    return new Response(
      JSON.stringify({ error: "canon_not_found" }),
      {
        status: 404,
        headers: { "content-type": "application/json; charset=utf-8" }
      }
    );
  }

  return new Response(response.body, {
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "public, max-age=300, s-maxage=3600"
    }
  });
}
