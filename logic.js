// Asynchronous function to load and display schedule content for a specific group
async function loadContent(group) {
  // Sample scheduleData to initialize the timetable structure
  const scheduleData = [
    ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    ["08:00 - 08:50", "", "", "", "", ""],
    ["09:00 - 09:50", "", "", "", "", ""],
    ["10:15 - 11:05", "", "", "", "", ""],
    ["11:15 - 12:05", "", "", "", "", ""],
    ["15:00 - 15:50", "", "", "", "", ""],
    ["16:00 - 16:50", "", "", "", "", ""],
    ["17:00 - 17:50", "", "", "", "", ""],
    ["18:15 - 19:05", "", "", "", "", ""],
    ["19:15 - 20:05", "", "", "", "", ""],
    ["20:15 - 21:05", "", "", "", "", ""]
  ];

  // Initialize an empty timetable object
  const timetable = {};

  // Load JSON data for the schedule and subject names
  const tensor = await load_json("./out/schedules.json");
  const subject_names = await load_json("./data/subject-name.json");

  // Define arrays for days and hours
  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
  const hours = [
    "08:00 - 08:50", "09:00 - 09:50", "10:15 - 11:05", "11:15 - 12:05",
    "15:00 - 15:50", "16:00 - 16:50", "17:00 - 17:50", "18:15 - 19:05",
    "19:15 - 20:05", "20:15 - 21:05"
  ];

  // Populate timetable with subjects and teachers based on tensor data
  for (const key in tensor) {
    let [real_key] = key.split("_");
    real_key = real_key.slice(2, -2);
    const [groupKey, dayIndex, hourIndex, subject, teacher] = real_key.split("', '");

    if (groupKey === group) {
      const day = days[parseInt(dayIndex) - 1];
      const hour = hours[parseInt(hourIndex) - 1];

      // Create necessary nested structures in timetable
      timetable[day] = timetable[day] || {};
      timetable[day][hour] = timetable[day][hour] || [];

      // Add subject and teacher information to the timetable
      timetable[day][hour].push([subject_names[subject], teacher]);
    }
  }

  // Fill the scheduleData array based on the timetable
  hours.forEach((hour, hourIndex) => {
    const rowData = [hour];
    days.forEach((day) => {
      const subjectsTeachers = timetable[day] && timetable[day][hour] ? timetable[day][hour] : [];

      // Format teacher names with a space before each capital letter
      if (subjectsTeachers.length > 0) {
        subjectsTeachers[0][1] = subjectsTeachers.map((subjectTeacher) => subjectTeacher[1].replace(/([A-Z])/g, " $1").trim()).join("<br>");
        const cellData = subjectsTeachers[0].map((subjectTeacher) => `<div>${subjectTeacher}</div>`).join("");
        rowData.push(cellData);
      } else {
        rowData.push("");
      }
    });
    scheduleData[hourIndex + 1] = rowData;
  });

  // Delete rows with all empty strings in the scheduleData
  const rowsToDelete = [];
  scheduleData.forEach((rowData, index) => {
    const isEmpty = rowData.slice(1).every(cellData => cellData === "");
    if (isEmpty) {
      rowsToDelete.push(index);
    }
  });
  rowsToDelete.reverse().forEach(index => scheduleData.splice(index, 1));

  // Get the content div element
  const contentDiv = document.getElementById("content");

  // Create a table element
  const table = document.createElement("table");

  // Iterate through scheduleData to create rows and cells
  scheduleData.forEach(rowData => {
    const row = table.insertRow();
    row.classList.add("custom-row");

    rowData.forEach(cellData => {
      const cell = row.insertCell();
      cell.innerHTML = cellData;
    });
  });

  // Merge cells with the same content in consecutive rows
  const rows = table.rows;
  for (let i = rows.length - 2; i >= 0; i--) {
    const row = rows[i];
    const cells = row.cells;
    for (let j = 0; j < cells.length; j++) {
      const cell = cells[j];
      const nextCell = rows[i + 1].cells[j];
      if (nextCell && cell.innerHTML === nextCell.innerHTML) {
        cell.rowSpan++;
        nextCell.hidden = true;
      }
    }
  }

  // Replace the content of the "content" div with the generated table
  contentDiv.innerHTML = "";
  
  // Create a title element
  const title = document.createElement("h1");
  title.innerHTML = `Schedule for group ${group}`;
  
  // Append title and table to the content div
  contentDiv.appendChild(title);
  contentDiv.appendChild(table);
}

// Asynchronous function to load JSON data from a specified path
async function load_json(path) {
  try {
    const response = await fetch(path);
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error loading JSON:", error);
    throw error; // Re-throw the error to be caught by the caller if necessary
  }
}
