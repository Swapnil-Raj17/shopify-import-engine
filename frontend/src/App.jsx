// import { useState } from "react";
// import { useEffect } from "react";

// import Papa from "papaparse";
// import axios from "axios";

// function App() {
//   const [rows, setRows] = useState([]);
//   const [loading, setLoading] = useState(false);

//   // Read CSV
//   const handleFile = (e) => {
//     const file = e.target.files[0];

//     Papa.parse(file, {
//       header: true,
//       skipEmptyLines: true,
//       complete: (result) => {
//         setRows(result.data);
//       }
//     });
//   };

//   // Update table cell
//   const updateValue = (index, key, value) => {
//     const updated = [...rows];
//     updated[index][key] = value;
//     setRows(updated);
//   };

//   // Send edited data to backend
//   const uploadData = async () => {
//     try {
//       setLoading(true);
//       await axios.post("http://localhost:8000/import/products", {
//         products: rows
//       });
//       alert("Products updated successfully!");
//     } catch (err) {
//       console.error(err);
//       alert("Upload failed");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div style={{ padding: 20 }}>
//       <h2>🛒 Shopify Import Engine</h2>

//       <input type="file" accept=".csv" onChange={handleFile} />

//       {rows.length > 0 && (
//         <>
//           <h3>CSV Preview (Editable)</h3>

//           <table border="1" cellPadding="5">
//             <thead>
//               <tr>
//                 {Object.keys(rows[0]).map((key) => (
//                   <th key={key}>{key}</th>
//                 ))}
//               </tr>
//             </thead>
//             <tbody>
//               {rows.map((row, i) => (
//                 <tr key={i}>
//                   {Object.keys(row).map((key) => (
//                     <td key={key}>
//                       <input
//                         value={row[key] || ""}
//                         onChange={(e) =>
//                           updateValue(i, key, e.target.value)
//                         }
//                         style={{ width: "120px" }}
//                       />
//                     </td>
//                   ))}
//                 </tr>
//               ))}
//             </tbody>
//           </table>

//           <br />

//           <button onClick={uploadData} disabled={loading}>
//             {loading ? "Uploading..." : "Update Shopify"}
//           </button>
//         </>
//       )}
//     </div>
//   );
// }

// export default App;




// import { useState } from "react";
// import { useEffect } from "react";
// import Papa from "papaparse";
// import axios from "axios";

// function App() {
//   const [rows, setRows] = useState([]);
//   const [loading, setLoading] = useState(false);

//   // Read CSV
//   const handleFile = (e) => {
//     const file = e.target.files[0];

//     Papa.parse(file, {
//       header: true,
//       skipEmptyLines: true,
//       complete: (result) => {
//         setRows(result.data);
//       }
//     });
//   };

//   // Update table cell
//   const updateValue = (index, key, value) => {
//     const updated = [...rows];
//     updated[index][key] = value;
//     setRows(updated);
//   };
//   const fetchProducts = async () => {
//   const res = await axios.get("http://localhost:8000/products");
//   setRows(res.data);
//   };


//   // Send edited data to backend
//   const uploadData = async () => {
//     try {
//       setLoading(true);
//       await axios.post("http://localhost:8000/import/products", {
//         products: rows
//       });
//       alert("Products updated successfully!");
//     } catch (err) {
//       console.error(err);
//       alert("Upload failed");
//     } finally {
//       setLoading(false);
//     }
//   };
//   useEffect(() => {
//   fetchProducts();

//   const interval = setInterval(() => {
//     fetchProducts();
//   }, 5000);

//   return () => clearInterval(interval);
// }, []);


//   return (
//     <div style={{ padding: 20 }}>
//       <h2>🛒 Shopify Import Engine</h2>

//       <input type="file" accept=".csv" onChange={handleFile} />

//       {rows.length > 0 && (
//         <>
//           <h3>CSV Preview (Editable)</h3>

//           <table border="1" cellPadding="5">
//             <thead>
//               <tr>
//                 {Object.keys(rows[0]).map((key) => (
//                   <th key={key}>{key}</th>
//                 ))}
//               </tr>
//             </thead>
//             <tbody>
//               {rows.map((row, i) => (
//                 <tr key={i}>
//                   {Object.keys(row).map((key) => (
//                     <td key={key}>
//                       <input
//                         value={row[key] || ""}
//                         onChange={(e) =>
//                           updateValue(i, key, e.target.value)
//                         }
//                         style={{ width: "120px" }}
//                       />
//                     </td>
//                   ))}
//                 </tr>
//               ))}
//             </tbody>
//           </table>

//           <br />

//           <button onClick={uploadData} disabled={loading}>
//             {loading ? "Uploading..." : "Update Shopify"}
//           </button>
//         </>
//       )}
//     </div>
//   );
// }

// export default App;


import { useState } from "react";
import axios from "axios";
import Papa from "papaparse";

function App() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);

  // Upload CSV
  const handleFile = (e) => {
    const file = e.target.files[0];

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (result) => {
        setRows(result.data);
      },
    });
  };

  // Update cell
  const updateValue = (i, key, value) => {
    const copy = [...rows];
    copy[i][key] = value;
    setRows(copy);
  };

  // Upload to backend
  const uploadCSV = async () => {
    const formData = new FormData();
    const csv = Papa.unparse(rows);
    const blob = new Blob([csv], { type: "text/csv" });

    formData.append("file", blob, "products.csv");

    await axios.post("http://localhost:8000/import/products", formData);
    alert("CSV Uploaded");
  };

  // Save to Shopify
  const saveRow = async (index) => {
    await axios.post(
      `http://localhost:8000/import/products/${index}/save`
    );
    alert("Saved to Shopify");
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>🛒 Shopify Import Tool</h2>

      <input type="file" accept=".csv" onChange={handleFile} />

      <button onClick={uploadCSV} style={{ marginLeft: 10 }}>
        Upload CSV
      </button>

      <table border="1" cellPadding="6" style={{ marginTop: 20 }}>
        <thead>
          <tr>
            {rows[0] &&
              Object.keys(rows[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {Object.keys(row).map((key) => (
                <td key={key}>
                  <input
                    value={row[key]}
                    onChange={(e) =>
                      updateValue(i, key, e.target.value)
                    }
                  />
                </td>
              ))}
              <td>
                <button onClick={() => saveRow(i)}>Save</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

