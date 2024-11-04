// $(document).ready(function () {
//     $('form').on('submit', function (event) {
//         event.preventDefault();

//         let url = $(this).attr('action'); // Uses the form's action attribute
//         console.log(url);
//         $.ajax({
//             type: 'POST',
//             url: url,
//             data: $(this).serialize(),

//             success: function (response) {
//                 console.log('Form submitted successfully:', response);

//                 // if (response.table_html) {
//                 //     $('.table-container').html(response.table_html);
//                 // }
//                 // if (response.message) {
//                 //     alert(response.message);
//                 // }
//             },
//             error: function (xhr, status, error) {
//                 console.error('Error submitting form:', error);
//             }
//         });
//     });
// });
