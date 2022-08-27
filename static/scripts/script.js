var myTimeout;
var gentime;
var dattime;
var custime;
var gen = document.getElementById("generate");
var dat = document.getElementById("dataorders");
var cus = document.getElementById("customers");
const ctx = document.getElementById('myChart').getContext('2d');
function myFunction(){
    $.ajax({
        type: "POST",
        data : {data:"postgres"},
        url: "/generate_get_data",
      }).done(function (data) {
        console.log(data);
        const obj = JSON.parse(data);
        xaxis=obj.xaxis;
        yaxis=obj.yaxis;
        console.log(yaxis);
   
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: yaxis, 
                datasets: [{
                    label: '# of Votes',
                    data: xaxis, // Data on Y axis
                    borderWidth: 1
                }]
            }
         });
      });


}
function generate() {
  console.log("in generate");
  $.ajax({
    type: "POST",
    data : {data:"postgres"},
    url: "/generate",
  }).done(function (data) {
    const obj = JSON.parse(data);
    xaxis=obj.xaxis;
    yaxis=obj.yaxis;
    ds=obj.ds;
    var x = document.getElementById("demo");
    var y = document.getElementById("demo1");
    var z = document.getElementById("demo2");


    if (x.style.display === "none") {
      x.style.display = "block";
      y.style.display = "none";
      z.style.display = "none";
    } else {
      x.style.display = "block";
    }
    let adata = document.getElementById("demo").innerHTML;
    document.getElementById("demo").innerHTML = adata + "<br />" + ds;
    console.log(data);
   
    var chartExist = Chart.getChart("myChart"); // <canvas> id
    if (chartExist != undefined)  
      chartExist.destroy(); 
      const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: yaxis, 
            datasets: [{
                label: '# of Votes',
                data: xaxis, // Data on Y axis
                borderWidth: 1
            }]
        }
     });
  });
}
function dataorder() {
  console.log("in input_data_orders");
  $.ajax({
    type: "POST",
    data : {data:"postgres"},
    url: "/input_data_orders",
  }).done(function (data) {
    // data = JSON.parse(data);
    var x = document.getElementById("demo");
    var y = document.getElementById("demo1");
    var z = document.getElementById("demo2");


    if (y.style.display === "none") {
      y.style.display = "block";
      x.style.display = "none";
      z.style.display = "none";
    } else {
      y.style.display = "block";
    }
    let adata = document.getElementById("demo1").innerHTML;
    document.getElementById("demo1").innerHTML = adata + "<br />" + data;
    //$('#output').text(data.output).show();
    console.log(data);
    //document.getElementById("output").innerHTML = data;
  });
}
function customer() {
  console.log("in customers");
  $.ajax({
    type: "POST",
    data : {data:"postgres"},
    url: "/input_customers",
  }).done(function (data) {
    // data = JSON.parse(data);
    var x = document.getElementById("demo");
    var y = document.getElementById("demo1");
    var z = document.getElementById("demo2");


    if (z.style.display === "none") {
      z.style.display = "block";
      y.style.display = "none";
      x.style.display = "none";
    } else {
      z.style.display = "block";
    }
    let adata = document.getElementById("demo2").innerHTML;
    document.getElementById("demo2").innerHTML = adata + "<br />" + data;
    //$('#output').text(data.output).show();
    console.log(data);
    //document.getElementById("output").innerHTML = data;
  });
}

function handlegenerate() {
  stopinsert();
  if (dat.innerHTML == "STOP") dat.innerHTML = "Generate Data Orders";
  if (cus.innerHTML == "STOP") cus.innerHTML = "Generate Customers";
  gentime = setInterval(generate, 1000);
}
function handledataorder() {
  stopinsert();
  if (gen.innerHTML == "STOP") gen.innerHTML = "Generate";
  if (cus.innerHTML == "STOP") cus.innerHTML = "Generate Customers";
  dattime = setInterval(dataorder, 1000);
}
function handlecustomer() {
  stopinsert();
  if (dat.innerHTML == "STOP") dat.innerHTML = "Generate Data Orders";
  if (gen.innerHTML == "STOP") gen.innerHTML = "Generate";
  custime = setInterval(customer, 1000);
}

function genclick() {
  console.log("CLICKED GEN!");
  console.log(gen.value);
  if (gen.innerHTML == "Generate") {
    gen.innerHTML = "STOP";
    handlegenerate();
  } else {
    console.log("CLICKED stop!");
    document.getElementById("generate").innerHTML = "Generate";
    clearInterval(gentime);
  }
//   handlegenerate();
};
function datclick() {
  if (dat.innerHTML == "Generate Data Orders") {
    dat.innerHTML = "STOP";
    handledataorder();
  } else {
    document.getElementById("dataorders").innerHTML = "Generate Data Orders";
    clearInterval(dattime);
  }
};
function cusclick() {
  if (cus.innerHTML == "Generate Customers") {
    cus.innerHTML = "STOP";
    handlecustomer();
  } else {
    document.getElementById("customers").innerHTML = "Generate Customers";
    clearInterval(custime);
  }
};

function stopinsert() {
  console.log("stopinsert");
  clearInterval(gentime);
  clearInterval(dattime);
  clearInterval(custime);
}