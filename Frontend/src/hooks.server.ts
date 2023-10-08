export const handle = async ({ event, resolve }) => {
  let response;
  if (event.url.pathname === "/") {
    response = new Response("Redirect", {
      status: 303,
      headers: { Location: "/home" },
    });
  } else {
    response = await resolve(event);
  }

  return response;
};
