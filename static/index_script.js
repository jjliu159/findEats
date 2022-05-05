let issuesElement = document.getElementById('content1');
//-------------------------------------------------
let allIssues = [
  {
    "name": "Your Local Favorites",
    "description": "Explore New York City’s popular neighborhood restaurants and chains. From local cafes to supermarkets, we support all as long as it is food! Make note of the goodie bags from the stores you enjoy and help support them in the future! ",
    "picture": "local_r.png",
    // "article" : "https://www.forbes.com/sites/forbestechcouncil/2020/06/23/facial-recognition-systems-security/?sh=874c6b723240"
  },
  {
    "name": "Free Reservation & Free Food",
    "description": "Search, reserve, and pick up! That’s all there is to it. No fees or tax attached. Simply search for an address, see what is available that you like, place a reservation, pick up the goodie bag, and enjoy! Reservation is based on first-come, first-serve. ",
    "picture": "food.png",
    // "article": "http://sitn.hms.harvard.edu/flash/2020/racial-discrimination-in-face-recognition-technology/"
  },
  {
    "name": "Help Reduce Food Waste",
    "description": "Join us in fighting against the 40 million tons of food being thrown away annually. With food waste making up around 20% of landfill weight, FindEats is here to connect store owners to direct consumers in efforts to reduce wastfulness. ",
    "picture": "rrr1.jpg",
    // "article": "https://www.technologyreview.com/2020/06/12/1003482/amazon-stopped-selling-police-face-recognition-fight/"
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

//   let article = document.createElement("A");
//   article.href = incomingJSON['article'];
//   newContentElement.appendChild(article);

  let newImage = document.createElement("IMG");
  newImage.classList.add("image");
  newImage.src = incomingJSON['picture'];
//   article.appendChild(newImage);
  newContentElement.appendChild(newImage);

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
