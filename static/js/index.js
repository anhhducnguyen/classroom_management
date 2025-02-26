document.addEventListener("DOMContentLoaded", function () {
    fetch("http://127.0.0.1:8000/api/schedules/")  // URL API của bạn
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("schedule-table");
            tableBody.innerHTML = ""; // Xóa dữ liệu cũ

            data.forEach(schedule => {
                const row = `
                    <tr>
                        <td>${schedule.id}</td>
                        <td>${schedule.class_assigned_name}</td>
                        <td>${schedule.teacher_name}</td>
                        <td>${schedule.day_of_week_display}</td>
                        <td>${schedule.session_display}</td>
                        <td>${schedule.start_time}</td>
                        <td>${schedule.end_time}</td>
                        <td>${schedule.room}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        })
        .catch(error => console.error("Lỗi khi tải dữ liệu:", error));
});