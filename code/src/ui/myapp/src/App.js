import './App.css';
import { Button, Table, FormControl, InputGroup, Form } from 'react-bootstrap';
import response from "./mockResponse.json"; // remove this post integration
import axios from "axios";
import { useState, useEffect, useMemo } from 'react';
import { actionURL } from './constants';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

function App() {

  const [showButton, setShowButton] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [folderPath, setFolderPath] = useState('');

  const [dataMap, setDataMap] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: 'id', direction: 'ascending' });
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredData, setFilteredData] = useState([]);
  const [model, setModel] = useState("gpt-4o-mini");

  //remove this post integration
  // useEffect(() => {
  //   const data = response.results;
  //   console.log("data from inital response", data);
  //   setDataMap(data);
  // }, [response]);

  const handleFolderChange = (e) => {
    setFolderPath(e.target.value);
  };

  const handleEmailProcessing = () => {
    setShowButton(false);
    setIsLoading(true);
    const payload = { "model": model, "folder_path": folderPath };
    axios.post(actionURL, payload)
      .then(response => {
        setIsLoading(false);
        const data = response?.data?.results;
        setDataMap(data);
        console.log('Post created:', response);
      })
      .catch(error => {
        setIsLoading(false);
        setShowButton(true);
        setFolderPath("");
        console.log(error);
      });
  }

  const extractData = (data) => (Object.keys(data).map(key => {
    return (<><span>{key + ': ' + data[key] + " ,"}</span><br></br></>);
  }));

  const sortedData = useMemo(() => {
    if (searchTerm) setFilteredData([]);
    let sortableItems = searchTerm !== "" ? [...filteredData] : [...dataMap];
    sortableItems.sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) {
        return sortConfig.direction === 'ascending' ? -1 : 1;
      }
      if (a[sortConfig.key] > b[sortConfig.key]) {
        return sortConfig.direction === 'ascending' ? 1 : -1;
      }
      return 0;
    });
    return sortableItems;
  }, [dataMap, sortConfig, searchTerm]);

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortArrow = (key) => {
    let arrowKeys = (<><span>&#8593;</span><span>&#8595;</span></>);
    if (searchTerm) arrowKeys = (<></>);
    else if (sortConfig.key === key) {
      if (sortConfig.direction === "ascending") arrowKeys = (<span>&#8593;</span>)
      else arrowKeys = (<span>&#8595;</span>)
    }
    return arrowKeys;
  }

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
    const filteredData = dataMap.filter((item) => {
      if (searchTerm !== "") {
        return JSON.stringify(item).toLowerCase().includes(searchTerm?.toLowerCase())
      }
    });
    setFilteredData(filteredData);
  };

  const displayData = (data) => {
    return typeof data === 'object' ? extractData(data) : typeof data === "boolean" ? data ? "Yes" : "No" : data;
  }

  const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(dataMap);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
    const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
    saveAs(blob, 'processed_data.xlsx');
  };
  
  const onModelSelection = (e) => {
    setModel(e.target.value);
  }

  return (
    <div className="App">
      <div className="App-header">
        <div style={{ padding: "15px" }}>
          <span>Email Classification and OCR</span>
        </div>
      </div>
      <div className="app-wrapper">
        {showButton && (
          <>
            <div className="app-desc">Read and interpret the email content and attachments. You are just a click away!</div>
            <div className="processButton">
              <div style={{fontWeight: 500}}>Model Type:</div>
              <div style={{ display: 'block', width: 300, padding: 30, paddingLeft: "5px" }}>
                <Form.Select aria-label="Choose a Model" defaultValue={model} onChange={onModelSelection}>
                  <option value="gpt-4o-mini">gpt-4o-mini</option>
                  <option value="llama3">llama3</option>
                </Form.Select>
              </div>
            </div>
            <div className="processButton1">
              <div style={{fontWeight: 500, paddingRight: "5px"}}>Folder Path:</div>
              <input className="folderInput" type="text" value={folderPath} placeHolder="Enter the folder path" onChange={handleFolderChange} />
              </div>
              <div className="processButton email-btn">
              <Button disabled={(folderPath === "" && !folderPath.includes("/"))} variant="primary" style={{ float: "left" }} onClick={handleEmailProcessing}>
                Process Email
              </Button>
            </div></>)}
        {isLoading && (<div className="pleaseWait">Please wait...your request is being processed</div>)}
        {!showButton && dataMap.length !== 0 && (
          <div style={{ float: "left", paddingBottom: "30px" }}>
            <h3 style={{ paddingBottom: "20px" }}>Results</h3>
            <Button style={{ float: "right", margin: "10px" }} onClick={exportToExcel}>Export to EXCEL</Button>
            <InputGroup className="mb-3">
              <FormControl
                placeholder="Find by..."
                value={searchTerm}
                onChange={handleSearch}
              />
            </InputGroup>
            <Table hover size="sm">
              <thead>
                <tr>
                  <th width="300">Email Name</th>
                  <th className="sortable-th" width="170" onClick={() => requestSort("Request Type")}>
                    Request Type {sortArrow("Request Type")} </th>

                  <th className="sortable-th" width="170" onClick={() => requestSort("Sub-Request Type")}>
                    Sub-Request Type {sortArrow("Sub-Request Type")}</th>
                  <th width="1300">Reasoning</th>
                  <th className="sortable-th" width="30" onClick={() => requestSort("Confidence")}>Confidence Score  {sortArrow("Confidence")}</th>
                  <th width="500">Key Fields</th>
                  <th width="300">Duplicate entry</th>
                </tr>
              </thead>
              <tbody>
                {sortedData.map((data, index) => (<tr className={index % 2 !== 0 ? "add-background" : ''}>
                  <td>{displayData(data["email"])}</td>
                  <td>{displayData(data["Request Type"])}</td>
                  <td>{displayData(data["Sub-Request Type"])}</td>
                  <td>{displayData(data["Reason"])}</td>
                  <td>{displayData(data["Confidence"])}</td>
                  <td>{displayData(data["Extracted Fields"])}</td>
                  <td>{displayData(data["duplicate"])}</td>
                </tr>
                ))}
              </tbody>
            </Table>
          </div>)}
      </div>
    </div>
  );
}

export default App;
