


const mysql = require('mysql2');
const dayjs = require('dayjs');

//Create a connection between the backend server and the database:
const db = mysql.createPool({
  host: "localhost",
  user: "root",
  password: "FRACAS@22",
  database: "labbee"

  //host : "92.205.7.122",
  //user : "beaLab",
  //password : "FIycjLM5BTF;",
  //database : "i7627920_labbee"

});

function JobcardsAPIs(app) {
  // app.post("/api/jobcard", (req, res) => {
  //   res.send("Hesdfghdf");
  // });


  const moment = require('moment');



  // Parse the date using moment.js
  //const formattedDate = moment(jcOpenDate, 'DD/MM/YYYY', true).format('YYYY-MM-DD');
  //console.log('2', formattedDate)


  // To add new jobcards to the database:
  app.post('/api/jobcard1', (req, res) => {

    const { jcNumber, dcNumber, jcOpenDate, poNumber, jcCategory, testInchargeName, companyName, customerNumber, customerSignature, projectName, sampleCondition, referanceDocs, jcStatus, jcCloseDate, jcText, observations } = req.body

    // const formattedDate = dayjs(jcOpenDate, 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD HH:mm:ss');
    // // const formattedCloseDate = dayjs(jcCloseDate, 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD HH:mm:ss');
    // const formattedCloseDate = jcStatus === 'Close' ? dayjs(jcCloseDate, 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD HH:mm:ss') : null;
    console.log('jcOpenDate is', jcOpenDate);
    const formattedDate = dayjs(jcOpenDate, 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD HH:mm:ss');
    let formattedCloseDate = null;


    if (jcStatus === 'Close') {
      formattedCloseDate = dayjs(jcCloseDate, 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD HH:mm:ss');
    }

    console.log('ggggggggg')
    const sql = `INSERT INTO jobcards(jc_number, dcform_number, jc_opendate, po_number, category, test_inchargename, company_name, customer_number, customer_signature, project_name, sample_condition, referance_document, jc_status, jc_closedate, jc_text, observations ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`;


    // console.log('SQL Query:', sql);
    console.log('Query Values:', [dcNumber, formattedDate, poNumber, jcCategory, testInchargeName, companyName, customerNumber, customerSignature, projectName, sampleCondition, referanceDocs, jcStatus, formattedCloseDate, jcText, observations]);


    db.query(sql, [jcNumber, dcNumber, jcOpenDate, poNumber, jcCategory, testInchargeName, companyName, customerNumber, customerSignature, projectName, sampleCondition, referanceDocs, jcStatus, formattedCloseDate, jcText, observations], (error, result) => {
      if (error) {
        console.log(error);
        return res.status(500).json({ message: 'Internal server error' });
      } else {
        return res.status(200).json({ message: 'Jobcards added successfully' });
      }
    });
  });


  // To delete the jobcards  from the table:
  app.delete("/api/getjobcard/:jc_number", (req, res) => {
    const jcnumber = req.params.jc_number;
    const deleteQuery = "DELETE FROM jobcards WHERE jc_number = ?";

    db.query(deleteQuery, [jcnumber], (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while deleting the module" });
      }
      res.status(200).json({ message: "jobcards data deleted successfully" });
    });
  });


  // To Edit the selected jobcards:
  app.post('/api/jobcard/:jc_number', (req, res) => {
    const { dcformnumber, jcopendate, ponumber, category, testinchargename, companyname, customernumber, customersignature, projectname, samplecondition, referancedocument } = req.body;
    const jc_number = req.params.jc_number; // Use jc_number instead of id

    // Parse the date using moment.js
    const formattedDate = moment(jcopendate, 'DD/MM/YYYY', true).format('YYYY-MM-DD');


    const sqlQuery = `
        UPDATE jobcards 
        SET 
          dcform_number = ?,
          jc_opendate = ?,
          po_number = ?,
          category = ?,
          test_inchargename = ?,
          company_name = ?,
          customer_number = ?,
          customer_signature = ?,
          project_name = ?,
          sample_condition = ?,
          referance_document = ? 
        WHERE jc_number = ?`;

    // Use an array to provide values for placeholders in the query
    const values = [
      dcformnumber,
      formattedDate,
      ponumber,
      category,
      testinchargename,
      companyname,
      customernumber,
      customersignature,
      projectname,
      samplecondition,
      referancedocument,
      jc_number // jc_number should be included in the values array
    ];

    db.query(sqlQuery, values, (error, result) => {
      if (error) {
        console.log(error);
        return res.status(500).json({ message: "Internal server error", result });
      } else {
        res.status(200).json({ message: "Jobcard updated successfully" });
      }
    });
  });


  // To fetch the jcnumber from the table 'jobcards'
  app.get('/api/getjobcard', (req, res) => {
    const sqlQuery = `SELECT jc_number FROM jobcards`;
    db.query(sqlQuery, (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while fetching data" })
      }
      res.send(result)
    })
  });


  // To fetch the data based on the jcnumber from the table 'jobcards'
  app.get('/api/getjobcardlist/:jc_number', (req, res) => {
    const jcnumber = req.params.jc_number;
    const sqlQuery = `SELECT  dcform_number, jc_opendate, po_number, category, test_inchargename,company_name, customer_number, customer_signature, project_name, sample_condition, referance_document FROM jobcards WHERE jc_number = ?`;

    db.query(sqlQuery, [jcnumber], (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while fetching data" })
      }
      res.send(result)
    })
  });


  // To fetch the last saved jcnumber  from the table jobcards data table:
  app.get("/api/getLatestjcnumber", (req, res) => {
    const latestjcnumberJT = "SELECT jc_number FROM jobcards ORDER BY id  DESC LIMIT 1 "
    db.query(latestjcnumberJT, (error, result) => {
      if (result.length === 0) {
        res.send(
          [
            {
              "jc_number": "2023-24/12-000",
            }
          ]
        )
      } else {
        res.send(result);
      }
    });
  });

  app.post("/api/getJCCount", (req, res) => {

    const { finYear } = req.body;

    let sql = `SELECT COUNT(*) FROM jobcards WHERE jc_number LIKE '${finYear}%'`

    db.query(sql, (error, result) => {
      if (error) {
        console.log(error);
        return res.status(500).json(error)
      }
      else {
        return res.status(200).json(result[0]['COUNT(*)'])
      }
    });
  });




  // To add new eutdetails to the database:
  app.post('/api/eutdetails', (req, res) => {
    const { jcNumber, nomenculature, eutdescription, qty, partno, modelno, serialno } = req.body;

    const sql = `INSERT INTO eutdetails (jc_number,nomenculature, eut_description, qty, part_no, model_no, serial_no) VALUES (?,?,?,?,?,?,?)`;

    db.query(sql, [jcNumber, nomenculature, eutdescription, qty, partno, modelno, serialno], (error, result) => {
      if (error) {
        console.log(error);
        return res.status(500).json({ message: 'Internal server error' });
      } else {
        return res.status(200).json({ message: 'eutdetails added successfully' });
      }
    });
  });

  // To delete the eutdetails  from the table:
  app.delete("/api/geteutdetails/:jc_number", (req, res) => {
    const jcnumber = req.params.jc_number;
    const deleteQuery = "DELETE FROM eutdetails WHERE jc_number = ?";

    db.query(deleteQuery, [jcnumber], (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while deleting the module" });
      }
      res.status(200).json({ message: "eutdetails data deleted successfully" });
    });
  });

  // To Edit the selected eutdetails:
  app.post('/api/eutdetails/:jc_number', (req, res) => {
    const { nomenculature, eutdescription, qty, partno, modelno, serialno } = req.body;
    const jc_number = req.params.jc_number; // Use jc_number instead of id

    const sqlQuery = `
        UPDATE eutdetails 
        SET 
          nomenculature = ?, 
          eut_description = ?, 
          qty = ?, 
          part_no = ?,
          model_no = ?,
          serial_no = ?
        WHERE jc_number = ?`;

    // Use an array to provide values for placeholders in the query
    const values = [
      nomenculature,
      eutdescription,
      qty,
      partno,
      modelno,
      serialno,
      jc_number
    ];

    db.query(sqlQuery, values, (error, result) => {
      if (error) {
        console.log(error);
        return res.status(500).json({ message: "Internal server error", result });
      } else {
        res.status(200).json({ message: "eutdetails updated successfully" });
      }
    });
  });


  // To fetch the jcnumber from the table 'eutdetails'
  app.get('/api/geteutdetails', (req, res) => {
    const sqlQuery = `SELECT jc_number FROM eutdetails`;
    db.query(sqlQuery, (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while fetching data" })
      }
      res.send(result)
    })
  });

  // To fetch the data based on the jcnumber from the table 'eutdetails'
  app.get('/api/geteutdetailslist/:jc_number', (req, res) => {
    const jcnumber = req.params.jc_number;
    const sqlQuery = `SELECT  nomenculature, eut_description, qty, part_no, model_no, serial_no FROM eutdetails WHERE jc_number = ?`;

    db.query(sqlQuery, [jcnumber], (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while fetching data" })
      }
      res.send(result)
    })
  });






  // To add new tests to the database:
  app.post('/api/tests', (req, res) => {
    const { jcNumber, test, nabl, teststandard, referencedocument } = req.body;


    const sql = `INSERT INTO tests (jc_number, test, nabl, test_standard, reference_document) VALUES (?,?,?,?,?)`;

    db.query(sql, [jcNumber, test, nabl, teststandard, referencedocument], (error, result) => {
      if (error) {
        console.log(error);
        return res.status(500).json({ message: 'Internal server error' });
      } else {
        return res.status(200).json({ message: 'tests added successfully' });
      }
    });

  });

  // To delete the tests from the table:
  app.delete("/api/gettests/:jc_number", (req, res) => {
    const jcnumber = req.params.jc_number;
    const deleteQuery = "DELETE FROM tests WHERE jc_number = ?";

    db.query(deleteQuery, [jcnumber], (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while deleting the module" });
      }
      res.status(200).json({ message: "tests data deleted successfully" });
    });
  });



  // To Edit the selected tests:
  app.post('/api/tests/:jc_number', (req, res) => {
    const { test, nabl, teststandard, referencedocument } = req.body;
    const jc_number = req.params.jc_number;

    const sqlQuery = `
        UPDATE tests 
        SET 
          test = ?, 
          nabl = ?, 
          test_standard = ?, 
          reference_document = ? 
        WHERE jc_number = ?`;

    const values = [
      test,
      nabl,
      teststandard,
      referencedocument,
      jc_number
    ];

    db.query(sqlQuery, values, (error, result) => {
      if (error) {
        console.log(error);
        return res.status(500).json({ message: "Internal server error", result });
      } else {
        res.status(200).json({ message: "tests updated successfully" });
      }
    });
  });


  // To fetch the jcnumber from the table 'tests'
  app.get('/api/gettests', (req, res) => {
    const sqlQuery = `SELECT jc_number FROM tests`;
    db.query(sqlQuery, (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while fetching data" })
      }
      res.send(result)
    })
  });


  // To fetch the data based on the jcnumber from the table 'tests'
  app.get('/api/gettestslist/:jc_number', (req, res) => {
    const jcnumber = req.params.jc_number;
    const sqlQuery = `SELECT  test, nabl, test_standard, reference_document FROM tests WHERE jc_number = ?`;

    db.query(sqlQuery, [jcnumber], (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while fetching data" })
      }
      res.send(result)
    })
  });



  // To add new testdetails to the database:
  app.post('/api/testdetails', (req, res) => {
    const { jcNumber, test, chamber, eutserialno, standard, startby, startdate, enddate, duration, endedby, remarks, reportno, preparedby, nabluploaded, reportstatus } = req.body;
    // console.log('llllllllllllllllllllllllll', jcNumber, test, chamber, eutserialno, standard, startby, startdate, enddate, duration, endedby, remarks, reportno, preparedby, nabluploaded, reportstatus);

    // Parse the date using moment.js
    // const formattedstartDate = moment(startdate, 'DD/MM/YYYY', true).format('%Y-%m-%d %H:%i:%s');
    const formattedstartDate = dayjs(startdate, 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD HH:mm:ss');
    const formattedendDate = dayjs(startdate, 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD HH:mm:ss');
    // const formattedendDate = moment(enddate, 'DD/MM/YYYY', true).format('%Y-%m-%d %H:%i:%s');
    // const formattedDuration = `${hours}:${minutes}:${seconds}`;

    const sql = `INSERT INTO testdetails (jc_number, test, chamber, eut_serial_no, standard, start_by, start_date, end_date, duration, ended_by, remarks, report_no, prepared_by, nabl_uploaded, report_status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`;

    // console.log('SQL Query:', sql);
    // console.log('Query Values:', [jcNumber, test, chamber, eutserialno, standard, startby, startdate, enddate, duration, endedby, remarks, reportno, preparedby, nabluploaded, reportstatus]);

    db.query(sql, [jcNumber, test, chamber, eutserialno, standard, startby, formattedstartDate, formattedendDate, duration, endedby, remarks, reportno, preparedby, nabluploaded, reportstatus], (error, result) => {
      if (error) {
        console.log(error);
        return res.status(500).json({ message: 'Internal server error' });
      } else {
        return res.status(200).json({ message: 'testdetails added successfully' });
      }
    });

  });



  // To delete the testdetails from the table:
  app.delete("/api/gettestdetails/:jc_number", (req, res) => {
    const jcnumber = req.params.jc_number;
    const deleteQuery = "DELETE FROM testdetails WHERE jc_number = ?";

    db.query(deleteQuery, [jcnumber], (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while deleting the module" });
      }
      res.status(200).json({ message: "testdetails data deleted successfully" });
    });
  });


  // To Edit the selected testdetails:
  app.post('/api/testdetails/:jc_number', (req, res) => {
    const { test, chamber, eutserialno, standard, startby, startdate, enddate, duration, endedby, remarks, reportno, preparedby, nabluploaded, reportstatus } = req.body;
    const jc_number = req.params.jc_number;

    const hours = req.body.hours || 0;
    const minutes = req.body.minutes || 0;
    const seconds = req.body.seconds || 0;

    // Parse the date using moment.js
    const formattedstartDate = moment(startdate, 'DD/MM/YYYY', true).format('YYYY-MM-DD');
    const formattedendDate = moment(enddate, 'DD/MM/YYYY', true).format('YYYY-MM-DD');
    const formattedDuration = `${hours}:${minutes}:${seconds}`;


    const sqlQuery = `
        UPDATE testdetails 
        SET 
          test = ?, 
          chamber = ?, 
          eut_serial_no = ?, 
          standard = ? ,
          start_by = ? ,
          start_date = ? ,
          end_date = ? ,
          duration = ? ,
          ended_by = ? ,
          remarks = ? ,
          report_no = ? ,
          prepared_by = ? ,
          nabl_uploaded = ? ,
          report_status = ? 
        WHERE jc_number = ?`;

    const values = [test, chamber, eutserialno, standard, startby, startdate, enddate, duration, endedby, remarks, reportno, preparedby, nabluploaded, reportstatus, jc_number
    ];

    db.query(sqlQuery, values, (error, result) => {
      if (error) {
        console.log(error);
        return res.status(500).json({ message: "Internal server error", result });
      } else {
        res.status(200).json({ message: "testdetails updated successfully" });
      }
    });
  });


  // To fetch the jcnumber from the table 'testdetails'
  app.get('/api/gettestdetails', (req, res) => {
    const sqlQuery = `SELECT jc_number FROM testdetails`;
    db.query(sqlQuery, (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while fetching data" })
      }
      res.send(result)
    })
  });


  // To fetch the data based on the jcnumber from the table 'testdetails'
  app.get('/api/gettestdetailslist/:jc_number', (req, res) => {
    const jcnumber = req.params.jc_number;
    const sqlQuery = `SELECT  test, chamber, eut_serial_no, standard, start_by, start_date, end_date, duration, ended_by, remarks, report_no, prepared_by, nabl_uploaded, report_status FROM testdetails  WHERE jc_number = ?`;

    db.query(sqlQuery, [jcnumber], (error, result) => {
      if (error) {
        return res.status(500).json({ error: "An error occurred while fetching data" })
      }
      res.send(result)
    })
  });
}


// // To add new users to the database:
// app.post('/api/users', (req, res) => {
//   const { id, name, email, password, role, allowedcomponents } = req.body;


//   const sql = `INSERT INTO labbee_users (id, name, email, password, role, allowed_components ) VALUES (?,?,?,?,?,?)`;

//   db.query(sql, [id, name, email, password, role, allowedcomponents], (error, result) => {
//     if (error) {
//       console.log(error);
//       return res.status(500).json({ message: 'Internal server error' });
//     } else {
//       return res.status(200).json({ message: 'users added successfully' });
//     }
//   });

// });



module.exports = { JobcardsAPIs }