import type { RequestHandler } from "./$types";
import { json } from "@sveltejs/kit";

export const POST: RequestHandler = async ({ request }) => {
  // get headers
  const body = await request.json();

  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      name: body.name,
      email: body.email,
      username: body.username,
      user_id: body.uid,
    },
  };
  const response = await fetch(
    "https://open-source-api-vqi1.onrender.com/signup",
    options
  );
  const data = await response.json();
  return json({ data });
};
