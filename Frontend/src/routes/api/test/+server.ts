import type { RequestHandler } from "./$types";
import { json } from "@sveltejs/kit";

export const GET: RequestHandler = async () => {
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      user_id: "14997667",
      username: "shabo55ing",
      email: "shaboing@gma5il.com",
      name: "shaboing55boing",
    },
  };
  const response = await fetch(
    "https://open-source-api-vqi1.onrender.com/signup",
    options
  );
  const data = await response.json();
  return json({ data });
};
