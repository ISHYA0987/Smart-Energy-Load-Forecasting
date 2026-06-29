document.addEventListener("DOMContentLoaded", () => {

    const canvas = document.getElementById("forecastChart");

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    // Gradient
    const gradient = ctx.createLinearGradient(0,0,0,350);

    gradient.addColorStop(0,"rgba(37,99,235,0.35)");
    gradient.addColorStop(1,"rgba(37,99,235,0)");

    // Highest Point
    const maxValue = Math.max(...values);

    const pointColors = values.map(v =>
        v === maxValue ? "#ef4444" : "#2563eb"
    );

    const pointRadius = values.map(v =>
        v === maxValue ? 7 : 4
    );

    new Chart(ctx,{

        type:"line",

        data:{

            labels:labels,

            datasets:[{

                data:values,

                borderColor:"#2563eb",

                backgroundColor:gradient,

                fill:true,

                borderWidth:3,

                tension:0.45,

                pointBackgroundColor:pointColors,

                pointBorderColor:"#fff",

                pointBorderWidth:2,

                pointRadius: values.map(v => v === maxValue ? 7 : 3),

                pointHoverRadius: values.map(v => v === maxValue ? 10 : 6),

                pointHoverRadius:9

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            interaction:{

                mode:"index",

                intersect:false

            },

            plugins:{

                legend:{

                    display:false

                },

                tooltip:{

                    backgroundColor:"#081326",

                    titleColor:"#fff",

                    bodyColor:"#fff",

                    padding:12,

                    cornerRadius:10,

                    displayColors:false,

                    callbacks:{

                        label:function(context){

                            return context.parsed.y + " Wh";

                        }

                    }

                }

            },

            scales:{

                x:{

                    grid:{

                        display:false

                    },

                    ticks:{

                        color:"#64748b"

                    }

                },

                y:{

                    grid:{

                        color:"#edf2f7"

                    },

                    ticks:{

                        color:"#64748b"

                    }

                }

            }

        }

    });

});