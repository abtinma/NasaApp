const { onRequest } = require("firebase-functions/v2/https");

let ssrServerServer;
let test;
exports.ssrServer = onRequest(async (request, response) => {
  if (!ssrServerServer) {
    ssrServerServer = require("./ssrServer/index").default;
  }
  return ssrServerServer(request, response);
});
