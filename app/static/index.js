const gallery = document.getElementById("gallery");

const characters_url = "http://127.0.0.1:8000/api/v1/characters"

async function getData(url){
    try {
        const response = await fetch(url);
        if(!response.ok){
            throw new Error(`Response status: ${response.status}`);
        }

        const json = await response.json();
        return json;

    }catch(error){
        console.log(error.message);
    }
}

const addElement = (name, surname, gender, age, roles, image, id, user, votes)=>{
    const newCard = document.createElement("div");
    newCard.className = "card";
    newCard.id = id;
    newCard.innerHTML = `<img src=${image}></img>
                        <h2>${name} ${surname}</h2>
                        <h3>age: ${age}</h3>
                        <h3>gender: ${gender}</h3>
                        <p>${roles}</p>
                        <p>Votes: ${votes}</p>`;
    
    const userProfile = document.createElement("div");
    userProfile.className = "user-profile";
    userProfile.id = user.id;
    if(user.profile_picture){
        userProfile.innerHTML = `<img src=${user.profile_picture}></img>
                                <p>${user.username}</p>`
    }else{
        userProfile.innerHTML = `<img src="https://i.pinimg.com/736x/16/98/4f/16984f82ecc712db4dc78b9a66cf09bd.jpg"}></img>
                                <p>${user.username}</p>`
    }
    

    newCard.append(userProfile)

    gallery.appendChild(newCard);

}

getData(characters_url)
    .then(characters => {
        if (characters && characters.length > 0) {
            characters.forEach(character => {
                const { name, surname, gender, age, roles, image, id, user, votes } = character;
                addElement(name, surname, gender, age, roles, image, id, user, votes);
            });
        } else {
            console.log("No characters found");
        }
    })
    .catch(error => {
        console.error("Error fetching data:", error);
    });