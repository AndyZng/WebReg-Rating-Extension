var profName;
var classNum;
var classDesc;
var numArr;
var parent;
let capesData, rmpData, capesRows, rmpRows;
var firstCapes;
var origProfName;
var otherProfName;
var onOFF;
var infoDisp = document.createElement("div");
var isShown;
async function getData() {
  const rmpResponse = await fetch(chrome.runtime.getURL("rmp_data_without_empty_lines.csv"));
  rmpData = await rmpResponse.text();
  const capesResponse = await fetch(chrome.runtime.getURL("capes_data.csv"));
  capesData = await capesResponse.text();
  rmpRows = rmpData.split('\n');
  capesRows = capesData.split('\n');
}
getData();
const isExactMatch = (course, elem) => {
  return new RegExp(course + '\\b').test(elem);
}

  document.addEventListener("mouseover", function (event) {
    var rmpFound = false;
    var firstFound = false;
    var capesInfo, rmpInfo;
    var target = event.target;
    if (target.matches('td[aria-describedby="search-div-b-table_PERSON_FULL_NAME"]')) {
      profName = target.textContent.trim();
      parent = target.parentNode;
      if (profName == "Instructor" || profName == "Staff" || profName == "") {
        profName = null;
      }
      if (parent) {
        classDesc = parent.querySelector('td[role="gridcell"][aria-describedby="search-div-b-table_colsubj"]');
        classDesc = classDesc.textContent.trim()
        classDesc = classDesc.split(/\s+/);
        classDesc = classDesc[0] + " " + classDesc[1];
      }
      if (profName) {
        origProfName = profName;
        profName = profName.split(',').map(item => item.trim());
        length = profName.length;
        profName = profName[length - 1] + " " + profName[length - 2];
        otherProfName = profName.split(" ");
        opnLen = otherProfName.length;
        otherProfName = otherProfName[0] + " " + otherProfName[opnLen - 1];
        for (let i = 0; i < rmpRows.length; i++) {
          const rmpElem = rmpRows[i];
          if ((rmpElem.includes(profName) || rmpElem.includes(otherProfName)) && !rmpElem.includes("N/A")) {
            rmpInfo = rmpElem;
            rmpFound = true;
            break;
          }
        }
        for (let i = 0; i < capesRows.length; i++) {
          const capesElem = capesRows[i];
          if (!firstFound && isExactMatch(classDesc, capesElem)) {
            firstCapes = capesElem;
            firstFound = true;
          }
          if (isExactMatch(classDesc, capesElem) && capesElem.includes(origProfName)) {
            capesInfo = capesElem;
            firstFound = false;
            break;
          }
        }
        if (firstFound) {
          capesInfo = firstCapes;
        }
        if (!rmpFound) {
          console.log("no ratings");
        }
      }
      if(profName){
        rmpInfo = rmpInfo.match(/("[^"]*"|[^",]*)(?=\s*,|\s*$)/g);
        capesInfo = capesInfo.match(/("[^"]*"|[^",]*)(?=\s*,|\s*$)/g);
        var dispName = document.getElementById("name");
        var dispRating = document.getElementById("rating");
        var dispWTA = document.getElementById("wta");
        var dispDiff = document.getElementById("difficulty");
        var dispTags = document.getElementById("tags");
        var dispTerm = document.getElementById("term");
        var dispCourse = document.getElementById("course");
        var dispRcmdClass = document.getElementById("rcmdClass");
        var dispRcmdIns = document.getElementById("rcmdIns");
        var dispStdyHrs = document.getElementById("stdyHrs");
        var dispAvgGrade = document.getElementById("avgGrade");
        dispName.textContent = rmpInfo[0];
        dispRating.textContent = rmpInfo[2];
        dispWTA.textContent = rmpInfo[4];
        dispDiff.textContent = rmpInfo[6];
        dispTags.textContent = rmpInfo[8];
        dispTerm.textContent = capesInfo[2];
        dispCourse.textContent = capesInfo[4];
        dispRcmdClass.textContent = capesInfo[6];
        dispRcmdIns.textContent = capesInfo[8];
        dispStdyHrs.textContent = capesInfo[10];
        dispAvgGrade.textContent = capesInfo[12];
        infoDisp.id = "infoDisplay";
        infoDisp.textContent = `Name: ${rmpInfo[0]}\n`; 
        document.body.appendChild(infoDisp);
        infoDisp.style.display = 'block';
        isShown = true;
      }
    }
    profName = null;
  });
  
  document.addEventListener("mouseout", function () {
    if(isShown){
      infoDisp.style.display = 'none';
      infoDisp.textContent = null; 
    }
  }
  )
  



