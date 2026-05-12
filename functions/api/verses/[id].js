export async function onRequestGet({ params, request }) {
  const canonUrl = new URL("/canon.json", request.url);
  const response = await fetch(canonUrl);

  if (!response.ok) {
    return json({ error: "canon_not_found" }, 404);
  }

  const canon = await response.json();
  const requestedId = String(params.id || "").toUpperCase();
  const record = canon.records.find((item) => item.id === requestedId);

  if (!record) {
    return json({ error: "verse_not_found", id: requestedId }, 404);
  }

  return json(record, 200, {
    "cache-control": "public, max-age=300, s-maxage=3600"
  });
}

function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      ...headers
    }
  });
}
