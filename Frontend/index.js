// -----> Declaring all variables

var DOMstrings = {
    easy : '#easy',
    mediam: '#medium',
    hard: '#hard',
    cate: '.category',
    entry: '#entry',
    btn: '.play-btn',
    gblock: '#gridblock',
    gridTable: '#myTable',
    name:'.naming',
    inputName : '.input-name',
    dataStruc : '#matrix',
    time : '.time',
    flag: '.grid-flag'
};

var table = document.getElementById("myTable");
var matrix = document.getElementById("matrix");
var myVar , level = 'none',str ,time=0;

// ---> check value function
var checkVal = function(val){
    if(val === '.'){return '';}
    
}

// ---> timer to float function
var covertTime = function(timer){
    var time;
   time = timer.split(':');
   return parseInt(time[0])+parseInt(time[1]);
}

// ---> creating grid and data structure
function createGrid(a , b){
    for (var i=0; i<a; i++) {
        row = table.insertRow(i); 
        for (var j=0; j<b; j++) {
             cell = row.insertCell(j);  
             cell.id =  'cellNo-'+i +'/'+j ;  
             cell.setAttribute('clicked' ,'false');
        }
    }  
}

function createData(data,a,b){    
    for (var i=0; i<a; i++) {
        row = matrix.insertRow(i);  
        for (var j=0; j<b; j++) {
             cell = row.insertCell(j);  
             cell.innerHTML = checkVal(data.board[i][j]);
             cell.id =  'cellNo:'+i +'/'+j; 
        }
    }   
}

// ---> emptying the table
 var emptyTable = function(level){
     
    if(level === 'empty'){
        console.log('launchig....');

    } else if(level === 'easy'){
        for(var i=0;i<10;i++){
          table.deleteRow(0);
          matrix.deleteRow(0);
        }
        console.log('launchig easy....');

    } else if(level === 'med'){
        for(var i=0;i<16;i++){
          table.deleteRow(0);
          matrix.deleteRow(0);
        }
        console.log('launchig med....');

    } else if(level === 'hard'){
        for(var i=0;i<19;i++){
          table.deleteRow(0);
          matrix.deleteRow(0);
        }
        console.log('launchig hard....');
    }
 }


// ---> function to generate Detail page
var askDetail = function(val){
    document.querySelector(DOMstrings.entry).classList.remove("none"); 

    document.querySelector(DOMstrings.gridTable).classList.remove("easy");
    document.querySelector(DOMstrings.dataStruc).classList.remove("easy");

    document.querySelector(DOMstrings.gridTable).classList.remove("med");
    document.querySelector(DOMstrings.dataStruc).classList.remove("med");

    document.querySelector(DOMstrings.gridTable).classList.remove("hard");
    document.querySelector(DOMstrings.dataStruc).classList.remove("hard");

    if(val == 'easy'){
        createGrid(10,10);
        document.querySelector(DOMstrings.gridTable).classList.add("easy");
        document.querySelector(DOMstrings.dataStruc).classList.add("easy");
    }

    else if(val == 'med'){
        createGrid(16,16);
        document.querySelector(DOMstrings.gridTable).classList.add("med");
        document.querySelector(DOMstrings.dataStruc).classList.add("med");
    }

    else if(val == 'hard'){
        createGrid(19,30);
        document.querySelector(DOMstrings.gridTable).classList.add("hard");
        document.querySelector(DOMstrings.dataStruc).classList.add("hard");
    }
}

// ---> UI update fuction
var UIupdate = function(data,act,level){
    var max_row,max_col,ele ,ele1;
    if(level === 'easy'){ max_col =10; max_row =10;}
    else if(level === 'med'){ max_col =16; max_row =16;}
    else if(level === 'hard'){ max_col =30; max_row =19;}
    var row =  data.num_row;
    var col =  data.num_col;
     
    
    if(act == 1){
        ele = document.getElementById('cellNo-'+row+'/'+col);
        ele1 = document.getElementById('cellNo:'+row+'/'+col);
        ele.innerHTML='<img src="black_flag.png" alt="" class="grid-flag">';
        ele1.innerHTML = '#';
    }

    else if(act == -1){
        ele = document.getElementById('cellNo-'+row+'/'+col);
        ele1 = document.getElementById('cellNo:'+row+'/'+col);
        ele.innerHTML=' ';
        ele1.innerHTML=' ';
    }
    else if(act == 0){
        for (var i=0; i<max_row; i++){ 
            for (var j=0; j<max_col; j++){
                ele = document.getElementById('cellNo-'+i+'/'+j);
                ele1 = document.getElementById('cellNo:'+i+'/'+j);
                if(data.board[i][j] === "#"){
                   console.log("Hiflag");
                }
                else if(data.board[i][j] === "-1"){
                    ele.style.transform = "rotateY(180deg)";
                    ele.style.transform = "scale(0)";
                    ele.setAttribute('clicked','true') ;

                    if(ele1.innerHTML == '#'){
                        ele1.classList.add('fbomb-background');
                    }    
                    else
                        ele1.classList.add('bomb-background');

                    ele1.innerHTML = '<img src="black_bomb.png" alt="" class="grid-bomb">';
                   
                }
                else if(data.board[i][j] === "0"){
                    ele.style.transform = "rotateY(180deg)";
                    ele.style.transform = "scale(0)";
                    ele.setAttribute('clicked','true') ;
                    }
                else if(data.board[i][j] !== "."){
                    ele1.innerHTML = data.board[i][j];
                    ele.style.transform = "rotateY(180deg)";
                    ele.style.transform = "scale(0)";
                    ele.setAttribute('clicked','true') ;
                }    
            }
        }    
    }

    if(data.status == -1){
        pauseWatch();
        for (var i=0; i<max_row; i++) 
        for (var j=0; j<max_col; j++){
            ele = document.getElementById('cellNo-'+i+'/'+j);
            ele.setAttribute('clicked','true') ;   
        }

        setTimeout(
            function(){
                document.querySelector('.popup-lose').classList.remove('none');

                setTimeout(() =>{
                    document.querySelector('.popup-wrapper-lose').style.transform = "scale(1)";
                },500);

                setTimeout(() => {
                    document.querySelector('.popup-wrapper-lose').style.transform = "scale(0)";

                    setTimeout(() =>{
                        document.querySelector('.popup-lose').classList.add('none');
                    },500);

                }, 5000);
            },100);      
    }

    else if(data.status == 1){
        pauseWatch();
        for (var i=0; i<max_row; i++) 
        for (var j=0; j<max_col; j++){
            ele = document.getElementById('cellNo-'+i+'/'+j);
            ele.setAttribute('clicked','true') ;   
        }
        
        setTimeout(
            function(){
                document.querySelector('.popup').classList.remove('none');

                setTimeout(() =>{
                    document.querySelector('.popup-wrapper').style.transform = "scale(1)";
                },500);

                setTimeout(() => {
                    document.querySelector('.popup-wrapper').style.transform = "scale(0)";

                    setTimeout(() =>{
                        document.querySelector('.popup').classList.add('none');
                    },500);

                }, 5000);
            },100);             
    }      
}


// ---> grid btn animation
var btnGrid = function(event){
    var item,item2,itemID,act ;
    act = event.button;
    if(act == '0')
       act = 0;
    else act = 1;   
    time = document.querySelector(DOMstrings.time).innerHTML;
    item = event.target.parentNode.parentNode.parentNode.id ;
    item2 = event.target.parentNode.parentNode.parentNode.parentNode.id;

    if(item == 'myTable' || item2 == 'myTable'){
        if(item == 'myTable'){
            itemID = event.target.id;
           
        }
        else if(item2 == 'myTable'){
            itemID=event.target.parentNode.id;
        }
        ele = document.getElementById(itemID);
        if(itemID && ele.getAttribute('clicked') == 'false'){
            splitID = itemID.split('-');
            splitID = splitID[1].split('/');       
            updateBoard(splitID[0],splitID[1],str,act,time,level);
        }
    }
}


// ----> all the eventListeners

 // 1. easy game DOM
document.querySelector(DOMstrings.easy).addEventListener('click', function(){ 
    emptyTable(level);
    document.querySelector(DOMstrings.name).innerHTML = '';
    document.querySelector(DOMstrings.gblock).classList.add("none");
    stopWatch();
    askDetail('easy');
    level = 'easy';
});

 // 2. Medium game DOM
 document.querySelector(DOMstrings.mediam).addEventListener("click", function(){ 
    emptyTable(level);
    document.querySelector(DOMstrings.name).innerHTML = '';
    document.querySelector(DOMstrings.gblock).classList.add("none");
    stopWatch();
    askDetail('med');
    level = 'med';
});

  // 3. Hard game DOM
 document.querySelector(DOMstrings.hard).addEventListener("click", function(){ 
    emptyTable(level);
    document.querySelector(DOMstrings.name).innerHTML = '';
    document.querySelector(DOMstrings.gblock).classList.add("none");
    stopWatch();
    askDetail('hard');
    level = 'hard';
});

  // 4. PLAY button DOM
document.querySelector(DOMstrings.btn).addEventListener('click', function(){
    // a) toggling display none class
    document.querySelector(DOMstrings.entry).classList.add("none");
    document.querySelector(DOMstrings.gblock).classList.remove("none");

    // b) taking name as string
     str = document.querySelector(DOMstrings.inputName).value;
     console.log(str);
     if(str == '')
       str = ' Anonymous';
     document.querySelector(DOMstrings.name).innerHTML = '<div class="player-name">Player\'s Name: '+str+'</div>';
  
     // c) calling server API function  
    createBoard(level,str);  

    // d) starting time watch
    startWatch();
});

 // 5. clicking on board buttons
 document.querySelector(DOMstrings.gridTable).addEventListener('contextmenu', event => event.preventDefault());
 document.querySelector(DOMstrings.gridTable).addEventListener('mouseup', btnGrid);



//  stop watch 
    var minute = 0;
    var second = 0;
    var sec = '00';
    var min = '00';
   
function timer(){ 
    document.querySelector(DOMstrings.time).innerHTML =   min + ":"+ sec;

     if(second == 60){
         minute++;
         second = 0;
     } else
       second ++;
     
     if(second <10)
        sec = '0' + second;
     else
        sec = second;   
        
    if(minute <10)
        min = '0' + minute;
     else
        min = minute;    
}

function startWatch(){
    myVar = setInterval(timer,1000); 
}  

function stopWatch(){
    clearInterval(myVar);
     minute = 0;
     second = 0;
     sec = '00';
     min = '00';
     document.querySelector(DOMstrings.time).innerHTML =   min + ":"+ sec;
}

function pauseWatch(){
    clearInterval(myVar);
}


// ------> linking function

var createBoard = function(level,user_id){
    var num_row,num_col;
   if(level === 'easy'){ num_col =10; num_row =10;}
   else if(level === 'med'){ num_col =16; num_row =16;}
   else if(level === 'hard'){ num_col =30; num_row =19;}
   

    fetch('http://127.0.0.1:8000/ingame/create_board/', {
        method: 'post',
        body: JSON.stringify({
                "num_row":num_row,	/* num_row -> It is the number of rows in board*/
                "num_col":num_col,	/*# num_col -> It is the number of columns in board*/
                "user_id":user_id,
                "is_bot" :0,	//#user_id  -> Username
                "game_type" : (level == "easy") ? 1 : (level == "med") ? 2 : (level == "hard") ? 3 : -1
                }   )
    }
    )
    .then(function(response) {
    return response.json();
    })
    .then(function(data){
      createData(data,num_row,num_col);
    });
}

var updateBoard = function(row,col,user_id,action,timer,level){
    
    timer = covertTime(timer);
    fetch('http://127.0.0.1:8000/ingame/update_board/', {
          method: 'post',
          body: JSON.stringify({
				"num_row":row,	// num_row -> It is the row in board the user clicked
				"num_col":col,	// num_col -> It is the column in board the user clicked
				"action" :action,    // action  -> It is the action of the user
				"user_id":user_id,  // user id
				"timer": timer      // timer
				}
			)
         }
    )
    .then(function(response) {
            return response.json();
    })
    .then(function(data){
                UIupdate(data,data.action,level);
    });
}


