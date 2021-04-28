/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from "react";
import { Menu, Layout } from "antd";
import { Link } from "react-router-dom";

import { LoginButton } from "./loginButton";
import { LoggedInUser } from "./loggedInUser";

export function NavMenu() {
  return (
    <Layout.Header
      style={{
        background: "#fff",
        width: "100%",
        height: "66px",
        paddingLeft: "10px",
        paddingRight: "10px",
        zIndex: 10,
      }}
    >
      <div
        style={{
          display: "grid",
          width: "100px",
          height: "64px",
          overflow: "hide",
          alignContent: "center",
          float: "left",
        }}
      >
        <img
          style={{ maxHeight: "100px", maxWidth: "100px" }}
          src={
            "https://cdn.discordapp.com/attachments/809363612404678657/814798379913314304/a.gif"
          }
          alt="logo"
        />
      </div>
      <div style={{ float: "right" }}>
        <LoginButton />
      </div>
      <div style={{ float: "right", marginRight: "10px" }}>
        <LoggedInUser />
      </div>
      <Menu mode="horizontal" style={{ borderBottom: "3px solid #096dd9" }}>
        <Menu.Item style={{ borderBottom: "0px" }}>
          <Link to="/">Home</Link>
        </Menu.Item>
        <Menu.Item style={{ borderBottom: "0px" }}>
          <Link to="/websockets">Websockets</Link>
        </Menu.Item>
        <Menu.Item style={{ borderBottom: "0px" }}>
          <Link to="/Overlay">Overlay</Link>
        </Menu.Item>
      </Menu>
    </Layout.Header>
  );
}
