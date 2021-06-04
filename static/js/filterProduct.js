// // document.getElementById('ff').innerHTML = 'dffff'

// $(document).ready(function(){
//     $(".ajaxLoader").hide()
//     $(".form-check-input").on('click', function(){
//         var _filterObj = {};
//         $(".form-check-input").each(function(index, ele){
//             var _filterVal = $(this).val()
//             var _filterKey = $(this).data('filter')
//             _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(){
//                 return ele.value;
//             })
//         })
//         console.log(_filterObj)

//         // Run ajax 
//         $.ajax({
//             url:'/filter-data',
//             // method:'post',
//             data:_filterObj,
//             dataType:'json',
//             beforeSend:function(){
//                 $(".ajaxLoader").html('Loading....')
//             },
//             success:function(res){
//                 $(".ajaxLoader").hide()
//                 console.log(res)
//             }
//         })
//     })
// })


// // var countjson = JSON.parse({'fsdfd'})
// var countjson = {{ countjson|safe }}
// console.log(countjson + "------------ countjson--------------")
// console.log("------------ script workeed --------------")

// function func01(){
//   console.log("------------ Function working --------------")
//   checkBox01 = document.getElementById('checkbox01')
  
//   filteredProducts = document.getElementById('filteredProducts')
//   console.log(filteredProducts + "------------ filteredProducts div --------------")
  
//   sellingPrice = document.getElementById('sellingPrice')
//   console.log(sellingPrice + "------------ sellingPrices --------------")
  

//   // console.log("checkBox01.value: " + checkBox01.value)
//   if (checkBox01.checked == true) {
//     if (checkBox01.value < sellingPrice) {
//       filteredProducts.style.display = "block";
//       console.log("------------ filteredProducts div blocked --------------")
//     } else {
//       filteredProducts.style.display = "none";
//       console.log("------------ filteredProducts div hided --------------")
//     }
//     console.log("checkBox01.value: " + checkBox01.value)
//   }
// }