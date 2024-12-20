

        

maptilersdk.config.apiKey = 'uYWkJDbhNtRWBEHZdXE3';


const map = new maptilersdk.Map({
    alpha: true,
    stencil: true,
    failIfMajorPerformanceCaveat: false,
    preserveDrawingBuffer: false,
    antialias: false,
    container: 'map', 
    style: "6dd5ec7a-ab91-4860-a71c-58129939b59f",
    center: [44.0900, 43.5369],
    zoom: 7.28,
    pitch: 100,
    bearing: 8
});


const map1 = new maptilersdk.Map({
    alpha: true,
    stencil: true,
    failIfMajorPerformanceCaveat: false,
    preserveDrawingBuffer: false,
    antialias: false,
    container: 'map1', 
    style: "b8481259-9fa1-47a0-8663-496fbd3c976b",
    center: [44.8050, 41.7349],
    zoom: 10.90,
    pitch: 50,
    bearing: 8
});




const specificColors = [
                            'rgb(255, 255, 255)', 
                            'rgb(228, 228, 228)', 
                            'rgb(255, 255, 255)', 
                            'rgb(228, 228, 228)',  
                            'rgb(255, 255, 255)',  
                            'rgb(228, 228, 228)',
                            'rgb(255, 255, 255)',  
                            'rgb(228, 228, 228)',
                            'rgb(255, 255, 255)',  
                        ];



function updateData() 
{


            fetch('/api/stations/div_positions')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data)
                const jsond = data;
                $('.dataContainer').remove();
                $('.map_spot').remove();
                $('.square').remove();
                $('.diagonal').remove();
                // console.log(jsond);

                // allUrlSets.forEach(function (urls) {
                    jsond.forEach(function (item1) {
                    
                    let pixel;
                    
                    if (item1.map_status == 1){
                        pixel = map1.project([item1.longitude, item1.latitude]);
                        
                    }
                    else if(item1.map_status == 0){
                        pixel = map.project([item1.longitude, item1.latitude]);
                    }
    
                    const dataContainer = document.createElement('div');
                    dataContainer.className = 'dataContainer';
                    const spot= document.createElement('div');
    
                    spot.className = 'map_spot';
                    spot.style.left = `${pixel.x}px`;
                    spot.style.top = `${pixel.y}px`;
    
                    // for (let colors = 0; colors < specificColors.length; colors++) 
                    // {
                    //     setTimeout(() => {
                    //     spot.style.backgroundColor = specificColors[colors];
                    //     }, colors * 60); 
                    // }
                                        
                    const square= document.createElement('div');
                    const diagonal= document.createElement('div');
    
    
                    square.className = 'square';
                    diagonal.className = 'diagonal';
    
                    square.style.left = `${pixel.x + item1.line_left_right}px`;
                    square.style.top = `${pixel.y + item1.line_top_bottom}px`;
    
    
                    const first_div = document.createElement('div');
                    const second_div = document.createElement('div');
                    const p1 = document.createElement('p');
                    const p2 = document.createElement('p');
                    const a = document.createElement('a');
                    a.setAttribute('href', item1.Url);
    
    
                    dataContainer.appendChild(first_div);
                    dataContainer.appendChild(second_div);
                    second_div.appendChild(a);
                    a.appendChild(p1);
                    a.appendChild(p2);
                    p1.innerHTML = `PR : ${item1.PRECIP_RATE }`;
                    p2.innerHTML = `PA : ${item1.PRECIP_ACCUM }`;
                    first_div.className = "first_div";
    
                    first_div.id = item1.id;
                    second_div.className = "second_div";
                    first_div.style.height = item1.first_div_height+"px";
    
                    document.body.appendChild(dataContainer);
    
                    dataContainer.style.left = `${pixel.x + item1.left_right}px`;
                    dataContainer.style.top = `${pixel.y + item1.top_bottom}px`;
    
                    diagonal.style.transform = "rotate(" + item1.line_rotate + "deg)";
    
                    document.body.appendChild(square);
                    square.appendChild(diagonal);
                    document.body.appendChild(spot);     
                    
                    });
            
                // });
            })

}

function go_to_login_page(){

    window.location.replace('/login');

}

updateData();
setInterval(updateData, 5000);

