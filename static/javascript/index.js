function searchSongs() {
    let x = document.getElementById("searchInput").value;
    fetch('http://192.168.4.44:5000/search/' + x) .then(response => response.json()) .then(data => {
        document.getElementById("searchResults").textContent = "";
        console.log(data)
        i = 1

        songData = []

        for (let i = 0; i < data["tracks"]["items"].length; i ++) {
            name = data["tracks"]["items"][i]["name"];
            //Goal: to get all the artists or 2 of them and show them and not just one without the screen getting all messed up
            artist = data["tracks"]["items"][i]["artists"][0]["name"];
            
            if (data["tracks"]["items"][i]["artists"].length > 1) {
                artist = ""
                for (let s = 0; s < data["tracks"]["items"][i]["artists"].length; s ++) {
                    artist += `${data["tracks"]["items"][i]["artists"][s]["name"]}, `;
                }
                length = artist.length
                artist = artist.slice(0, (length-2));
            }

            image_pic = data["tracks"]["items"][i]["album"]["images"][0]["url"];
            track_id = data["tracks"]["items"][i]["id"];


            x = {"name": name,
                "artist": artist,
                "art": image_pic,
                "id": track_id}

            songData[i] = x
        }
    
        for (let i = 0; i < 6; i ++) {
            name = songData[i]["name"]
            artist= songData[i]["artist"]
            image_pic = songData[i]["art"]
            track_id = songData[i]["id"]

            item = document.createElement("div");
            item.id = "item" + i;
            item.classList.add("item")

            image = document.createElement("div");
            image.id = "image" + i;

            data = document.createElement("div");
            data.id = "data" + i;
            data.classList.add("data")

            img = document.createElement('img');
            img.src = image_pic; img.height = "75"; img.width = "75";

            songName = document.createElement("h3");
            songName.textContent = name; songName.style = "font-size: 20px; margin: 0px; height: 25px";

            if (name.length > 25) {
                name = name.slice(0, 25)
                name += "..."
                songName.textContent = name
            }

            if (window.innerWidth < 500) {
                name = name.slice(0, 12)
                name += "..."
                songName.textContent = name
            }

            songBy = document.createElement("p");
            songBy.textContent = "By: " + artist; songBy.style = "margin: 0px; font-size: 10px;"

            button_group = document.createElement("div")
            button_group.classList.add("button-group"); button_group.id = "button-group" + i;

            detail = document.createElement("button")
            detail.id = track_id;
            //icon link click
            icon_link = document.createElement("a")
            icon_link.href = `https://open.spotify.com/track/${track_id}`;
            icon_link.id = "iconlink" + i; icon_link.target = "_blank";

            icon = document.createElement("img")
            icon.src = "/static/images/spotify_logo.png"; icon.width = "19"; icon.height = "19";

            button_art = document.createElement("img")
            button_art.src = "static/images/open_in_window.png"; button_art.width = "19"; button_art.height = "19";

            document.getElementById("searchResults").appendChild(item)
            document.getElementById("item" + i).appendChild(image)
            document.getElementById("item" + i).appendChild(data)

            document.getElementById('image' + i).appendChild(img);

            document.getElementById("data" + i).appendChild(songName);
            document.getElementById("data" + i).appendChild(songBy);
            
            document.getElementById("data" + i).appendChild(button_group);
            
            document.getElementById("button-group" + i).appendChild(icon_link);
            document.getElementById("iconlink" + i).appendChild(icon);

            //document.getElementById("button-group" + i).appendChild(detail);

            button_group.innerHTML += `<button id='${track_id}' onclick='openData(this.id)'></button>`;

            document.getElementById(track_id).appendChild(button_art);

            
        }
    }) .catch(error => console.error(error)); 
}

function openData(clicked_id) {
    console.log(clicked_id)
    fetch('http://192.168.4.44:5000/detail/' + clicked_id) .then(response => response.json()) .then(data => {
        console.log(data);

        //clearing current html in detail
        document.getElementById("detail").textContent = ""

        //top div
        topInfo = document.createElement("div")
        topInfo.id = "topInfo";
        topInfo.classList.add("topInfo");
        document.getElementById("detail").appendChild(topInfo);

        image = document.createElement("img");
        image.src = data["art"]; image.width = "100"; image.height = "100";
        document.getElementById("topInfo").appendChild(image);

        dataDetail = document.createElement("div");
        dataDetail.id = "dataDetail";
        dataDetail.classList.add("data2");
        document.getElementById("topInfo").appendChild(dataDetail);

        songName = document.createElement("h2");
        songName.textContent = data["name"];
        songName.style = `font-size: 32px; font-style: normal; font-weight: 700; line-height: normal; margin: 0px;`;
        document.getElementById("dataDetail").appendChild(songName)

        artist = document.createElement("p");
        artist.textContent = data["artist"];
        artist.style = `font-size: 15px; font-style: normal; font-weight: 700; line-height: normal; margin: 0px;`;
        document.getElementById("dataDetail").appendChild(artist);

        mainDetail = document.createElement("div");
        mainDetail.classList.add("mainDetail");
        mainDetail.id = "mainDetail";

        mainDetail.innerHTML = `
        <p>
        Track Id: ${data["id"]}<br>
        <br>
        Release Date: ${data["release"]}<br>
        Album Type: ${data["album_type"]}<br>
        Number of Songs: ${data["num_tracks"]}<br>
        Disc Number: ${data["dis_num"]}<br>
        Duration: ${data["duration"]} sec<br>
        Explicit: ${data["explicit"]}<br>
        Popularity: ${data["popularity"]}<br>
        <br>
        Acousticness: ${data["acousticness"]}<br>
        Valence: ${data["valence"]}<br>
        <br>
        Tempo: ${data["tempo"]}<br>
        Time Signature: ${data["time_signature"]}<br>
        </p>
        `;

        document.getElementById("detail").appendChild(mainDetail);


        
            
    }) .catch(error => console.error(error)); 
}