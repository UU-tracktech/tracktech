/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from "react";
import { BrowserRouter, Route } from "react-router-dom";
import { useKeycloak } from "@react-keycloak/web";
import { Layout } from "antd";
import "./app.less";

import { NavMenu } from "./components/navbar";
import { NeedLogin } from "./pages/needLogin";
import { Home } from "./pages/home";
import { WebsocketUser } from "./pages/websocket";
import { OverlayVideo } from "./pages/overlayVideo";
import { WebsocketProvider } from "./components/websocketContext";

export function App() {
  const { keycloak } = useKeycloak();

  return (
    <Layout
      style={{
        width: "100vw",
        height: "100vh",
        display: "grid",
        gridTemplateRows: "auto 1fr",
      }}
    >
      <WebsocketProvider>
        <BrowserRouter key={1}>
          <NavMenu key={0} />
          {true ? ( //keycloak.authenticated
            <>
              <Route exact path="/">
                <Home />
              </Route>
              <Route path="/Websockets">
                <WebsocketUser />
              </Route>
              <Route path="/Overlay">
                <OverlayVideo />
              </Route>
            </>
          ) : (
            <NeedLogin />
          )}
        </BrowserRouter>
      </WebsocketProvider>
    </Layout>
  );
}
