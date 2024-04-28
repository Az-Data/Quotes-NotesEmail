function findLowestValueAndIncrement(sheet) {
  var data = sheet.getRange("A2:B" + sheet.getLastRow()).getValues(); // Assuming data starts from row 2, columns A and B

  var lowestValue = Number.MAX_VALUE;
  var lowestIndex = -1;

  // Find the lowest value and its index
  for (var i = 0; i < data.length; i++) {
    if (data[i][1] < lowestValue) {
      lowestValue = data[i][1];
      lowestIndex = i;
    }
  }

  if (lowestIndex !== -1) {
    var value = data[lowestIndex][0]; // Value from column 1
    var rowToUpdate = lowestIndex + 2; // Adding 2 to convert index to actual row number (assuming data starts from row 2)
    
    // Increment the value in column 2
    sheet.getRange(rowToUpdate, 2).setValue(lowestValue + 1);
    
    return value;
  } else {
    return null;
  }
}

function sendEmailWithSpreadsheetData() {

  // For Quotes gsheet
  // Access the gsheet by its ID
  var quotesSpreadsheet = SpreadsheetApp.openById('18th3Bn8gN2QghPd8O18r8C0AXcevnLALN-LQJptuO6A');
  var quotesSheet = quotesSpreadsheet.getSheets()[0];

  var value1 = findLowestValueAndIncrement(quotesSheet);

  // For Questions gsheet
  // Access the gsheet by its ID
  var questionsSpreadsheet = SpreadsheetApp.openById('1Cu_GH6QyhjeJpS1uGSE-AflgwtnePtH761cWhaR4a5s');
  var questionsSheet = questionsSpreadsheet.getSheets()[0];

  var value2 = findLowestValueAndIncrement(questionsSheet);

  // Compose the email message
  var subject = 'Quotes and Notes';
  var htmlBody = `
  <h2>Quote</h2>
  <p>${value1}</p>

  <h2>Question</h2>
  <p>${value2}</p>  
  `;

  // Send the email 
  GmailApp.sendEmail(
    'akfernandi@gmail.com', 
    subject, '', 
    {htmlBody: htmlBody}
  );
}




