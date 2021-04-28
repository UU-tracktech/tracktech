/*

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 */

import React from "react";
import { Button, Card } from "antd";
import { Layout } from "antd";
import { PlusOutlined } from "@ant-design/icons";

import { Grid, source } from "../components/grid";
import { CameraCard } from "../components/cameraCard";

export type indicator = "All" | "Selection" | "None";
type tracked = { id: number; name: string; image: string; data: string };
export function Home() {
  const [sources, setSources] = React.useState<source[]>();
  const [currentIndicator, setCurrentIndicator] = React.useState<indicator>(
    "All"
  );
  const [tracking, setTracking] = React.useState<tracked[]>([]);
  const [sourceSizes, setSourceSizes] = React.useState<Map<string, number>>(
    new Map()
  );

  const selectionRef = React.useRef(0);

  React.useEffect(() => {
    fetch(process.env.PUBLIC_URL + "/config.json").then((text) =>
      text.json().then((json) => {
        var nexId = 0;
        setSources(
          json.map((stream) => ({
            id: nexId++,
            name: stream.Name,
            srcObject: {
              src: stream.Forwarder,
              type: stream.Type,
            },
          }))
        );
      })
    );
  }, []);

  function setSize(sourceId: string, size: number) {
    setSourceSizes(new Map(sourceSizes.set(sourceId, size)));
  }

  return (
    <Layout.Content
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 4fr",
        gridAutoRows: "100%",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "5px",
          overflowY: "auto",
          display: "grid",
          gap: "5px",
        }}
      >
        <Card
          bodyStyle={{ padding: "4px", display: "flex" }}
          headStyle={{ padding: 0 }}
          size="small"
          title={
            <h2 style={{ margin: "0px 8px", fontSize: "20px" }}>Indicators</h2>
          }
        >
          <Button
            style={{ marginLeft: "4px" }}
            type={currentIndicator === "All" ? "primary" : "default"}
            onClick={() => setCurrentIndicator("All")}
          >
            All
          </Button>
          <Button
            style={{ marginLeft: "4px" }}
            type={currentIndicator === "Selection" ? "primary" : "default"}
            onClick={() => setCurrentIndicator("Selection")}
          >
            Selection
          </Button>
          <Button
            style={{ marginLeft: "4px" }}
            type={currentIndicator === "None" ? "primary" : "default"}
            onClick={() => setCurrentIndicator("None")}
          >
            None
          </Button>
        </Card>

        <Card
          bodyStyle={{ padding: "4px" }}
          headStyle={{ padding: 0 }}
          size="small"
          title={
            <h2 style={{ margin: "0px 8px", fontSize: "20px" }}>Selection</h2>
          }
        >
          <div>
            <Button onClick={async () => await addSelection()}>+</Button>
          </div>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(100px, 1fr))",
              gridAutoRows: "100px",
            }}
          >
            {tracking &&
              tracking.map((tracked) => (
                <img
                  alt="tracked person"
                  onClick={() => removeSelection(tracked.id)}
                  style={{ width: "100%", height: "100%", margin: "5px" }}
                  src={tracked.image}
                />
              ))}
          </div>
        </Card>

        <Card
          bodyStyle={{ padding: "4px" }}
          headStyle={{ padding: 0 }}
          size="small"
          title={
            <h2 style={{ margin: "0px 8px", fontSize: "20px" }}>Cameras</h2>
          }
          extra={<PlusOutlined style={{ marginRight: 10 }} />}
        >
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
            }}
          >
            {sources &&
              sources.map((source) => (
                <CameraCard
                  id={source.id}
                  title={source.name}
                  setSize={setSize}
                />
              ))}
          </div>
        </Card>
      </div>

      <div style={{ overflowY: "auto" }}>
        {sources && (
          <Grid
            sources={sources}
            sourceSizes={sourceSizes}
            setSize={(sourceId: string, size: number) =>
              setSize(sourceId, size)
            }
            indicator={currentIndicator}
          />
        )}
      </div>
    </Layout.Content>
  );

  async function addSelection() {
    const pictures = ["car", "guy", "garden"];
    const picture = pictures[Math.floor(Math.random() * pictures.length)];

    var result = await fetch(process.env.PUBLIC_URL + `/${picture}.png`);
    var blob = await result.blob();
    var reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === "string") {
        console.log(reader.result);
        setTracking(
          tracking.concat({
            id: selectionRef.current++,
            name: "abc",
            image: reader.result,
            data: "",
          })
        );
      }
    };
    reader.readAsDataURL(blob);
  }

  function removeSelection(id: number) {
    setTracking(tracking.filter((tracked) => tracked.id !== id));
  }
}
