const fetchAppointmentData = async (pet_id) => {
    const res = await fetch(`/api/pets/${pet_id}/`)
    const data = await res.json()
    return data.appointments.slice(-5)
    // return data.filter(appointment => appointment.pet == pet_id)
}

const extractInfo = (appointmentInfo) => {
    return appointmentInfo.map(appointment => {
        return {
            weight: Number(appointment.weight),
            temperature: Number(appointment.temperature),
            breathing_frequency: appointment.breathing_frequency,
            heart_rate: appointment.heart_rate,
            created: appointment.created
        }
    })
}

document.addEventListener('DOMContentLoaded', async () => {
    let appointmentInfo = await fetchAppointmentData(document.getElementById('pet-data').dataset.id)
    if (appointmentInfo.length < 5) return
    proccessedAppointmentInfo = extractInfo(appointmentInfo)
    console.log(proccessedAppointmentInfo)

    labels = appointmentInfo.map(item => item.created)
    console.log(labels)

    const ctx = document.getElementById('myChart');
    const charInfo = {
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
        borderWidth: 1
    }

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Weight (kg)',
                    data: appointmentInfo.map(item => item.weight),
                    ...charInfo
                },
                {
                    label: 'Temperature (°F)',
                    data: appointmentInfo.map(item => item.temperature),
                    ...charInfo
                },
                {
                    label: 'Heart rate (bpm)',
                    data: appointmentInfo.map(item => item.heart_rate),
                    ...charInfo
                },
                {
                    label: 'Breathing frequency (breaths/min)',
                    data: appointmentInfo.map(item => item.breathing_frequency),
                    ...charInfo
                },
            ]
        },
        // options: {
        //     scales: {
        //         y: {
        //             beginAtZero: true
        //         }
        //     }
        // }
    });
})