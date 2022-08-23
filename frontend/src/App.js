import React, { useState, useEffect } from "react";
import './App.css';
import {Row, Col} from 'react-bootstrap';

const API = process.env.REACT_APP_API;

function App() {

  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [showRes, setShowRes] = useState(false);

  // useEffect(() => {
  //   console.log(query);
  // }, [query]);

  const search = async (e) => {
    e.preventDefault();
    // console.log(data);

    const res = await fetch(`${API}/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
            query:query
        }),
      });
    const data = await res.json();
    if (res.ok) {
        setResults(data);
        setShowRes(true);
    } else {
        console.log("Failed!");
    }
  }

  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <a className="navbar-brand">Question Matching</a>
        </div>
      </nav>
      <br></br>
      <div className="container p-4">
        <Row className="align-items-center">
          <Col md={{ span: 6, offset: 2 }}>
            <input className="form-control me-sm-2" type="text" placeholder="Search" value={query} onChange={e => {
              setShowRes(false);
              setQuery(e.target.value);
            }}></input>
          </Col>
          <Col md="auto">
            <button className="btn btn-primary my-2 my-sm-0" type="submit" onClick={search}>Search</button>
          </Col>
        </Row>
        {
          showRes &&
          <Row className="align-items-center pt-3">
            <Col md={{ span: 6, offset: 2 }}>
              <table className="table table-striped">
              <tbody>
                {results.map((res, index) => (
                  <tr key={index}>
                    <td>{index+1}</td>
                    <td>{res}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            </Col>
          </Row>
        }
      </div> 
    </div>
  );
}

export default App;
