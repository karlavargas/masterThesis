
var topics = ["architecture","arts","film","literature","music","performing arts","visual arts","africa","asia","city","country","earth","europe","geography","land","north america","oceania","sea","south america","ancient history","civilization","history","history of art","history of science","history of the world","modern history","post-classical history","prehistory","book","clothing","communication","death","emotion","entertainment","ethnic group","food","house","human sexuality","personal life","sleep","time","writing","arithmetic","geometry","mathematics","number","statistics","ethics","knowledge","logic","mind","mythology","philosophy","religion","animal","astronomy","atom","biology","cell","chemical element","chemistry","climate","disease","electricity","energy","human","life","medicine","nature","physics","plant","psychology","science","universe","water","business","community","crime","culture","education","employment","family","government","law","language","money","politics","popular culture","society","war","agriculture","computer","construction","engineering","fire","industry","manufacturing","technology","tool","transport"];


var search_results = "";
var fs = require('fs');
var page = require('webpage').create();
page.settings.userAgent = 'SpecialAgent';

function search(url,callback){
    console.log(url);
    page.open(url, function(status,resultNumber){
        if (status !== 'success') {
            console.log('Unable to access network');
        } else {
            var ua = page.evaluate(function() {
                return document.getElementById('resultStats').textContent;
            });
            var result = ua.split(" ");
        }
        resultNumber = result[2];
        callback(resultNumber);
    });
    return true;
}

function get_url(i,j){
    var url = "";
    var splittedI = topics[i].split(" ");
    if(splittedI.length > 1){
        url = "\\\""+topics[i]+"\\\"";
    }
    else{
        url = topics[i];
    }
    var splittedJ = topics[j].split(" ");
    if(splittedJ.length > 1){
        url += "+\\\""+topics[j]+"\\\"";
    }
    else{
        url += "+"+topics[j];
    }
    return "http://www.google.com/search?q="+url;
}

function start_search(begin,end){
    var ulr = "";
    var timeoutsInterval = 5000; 
    var nextTimeoutDelay = 0;
    for(i = begin; i < end; i++){
        for(j = 0; j < 3; j++){
            url = get_url(i,j);
            setTimeout(function(){
                search(url,function(result){   
                    console.log(result);
                    cadena = " "+"["+i+","+j+"]\n";
                    output = result+cadena; 
                    fs.write("output.txt",output,'a');
                });},nextTimeoutDelay);
            nextTimeoutDelay += timeoutsInterval;
        }
    }
}

start_search(0,10);