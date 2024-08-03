import React, { useState, useEffect } from "react";
import axios from "axios";
import { db } from "./firebase";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [results, setResults] = useState([]);
  const [faces, setFaces] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const facesCollection = await db.collection("faces").get();
      setFaces(facesCollection.docs.map((doc) => doc.data()));
    };
    fetchData();
  }, []);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await axios.post(
        "http://localhost:5000/recognize",
        formData
      );
      setResults(response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="App">
      <h1>Face Recognition</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      <ul>
        {results.map((result, index) => (
          <li key={index}>{result.name}</li>
        ))}
      </ul>
      <h2>Known Faces</h2>
      <ul>
        {faces.map((face, index) => (
          <li key={index}>{face.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
