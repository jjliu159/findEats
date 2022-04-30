let issuesElement = document.getElementById('content1');
//-------------------------------------------------
let allIssues = [
  {
    "name": "Your Local Favorites",
    "description": "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia,",
    "picture": "local_r.png",
    "article" : "https://www.forbes.com/sites/forbestechcouncil/2020/06/23/facial-recognition-systems-security/?sh=874c6b723240"
  },
  {
    "name": "Free Reservation & Free Food",
    "description": "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia,",
    "picture": "food.png",
    "article": "http://sitn.hms.harvard.edu/flash/2020/racial-discrimination-in-face-recognition-technology/"
  },
  {
    "name": "Help Reduce Food Waste",
    "description": "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia,",
    "picture": "rrr1.jpg",
    "article": "https://www.technologyreview.com/2020/06/12/1003482/amazon-stopped-selling-police-face-recognition-fight/"
  }
]
//-------------------------------------------------
for (var i = 0; i < allIssues.length; i++) {
  createElementProper(allIssues[i]);
}
//-------------------------------------------------
function createElementProper(incomingJSON) {

  let newContentElement = document.createElement("DIV");
  newContentElement.classList.add('contentItem');

  let article = document.createElement("A");
  article.href = incomingJSON['article'];
  newContentElement.appendChild(article);

  let newImage = document.createElement("IMG");
  newImage.classList.add("image");
  newImage.src = incomingJSON['picture'];
  article.appendChild(newImage);

  let newContentName = document.createElement("H3");
  newContentName.classList.add("name");
  newContentName.innerText = incomingJSON['name'];
  newContentElement.appendChild(newContentName);

  let newContentDes = document.createElement("P");
  newContentDes.classList.add("descript");
  newContentDes.innerText = incomingJSON['description'];
  newContentElement.appendChild(newContentDes);


  issuesElement.appendChild(newContentElement);

};
