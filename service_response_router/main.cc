#include <iostream>
#include <uwebsockets/App.h>

int main() {
  uWS::App().get("/*", [](auto* res, auto* req) {
    res->end("Hello from response router");
  })
  .listen(9001, [](auto* token) {
    if (token) std::cout << "Server is listening on port 9001" << std::endl;
    else std::cerr << "Failed to listen on port 9001" << std::endl;
  })
  .run();

  return 0;
}