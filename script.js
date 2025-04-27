/* script.js */
document.addEventListener('DOMContentLoaded', function() {

  const SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQqnVCJkYL6-nHK4Bt6JMDLAGHygCbpRb3vOmuXLOpO5D7qGFiR84InumQY8HjEjVTDbKfcsxIx2a9k/pub?gid=152263470&single=true&output=csv';

  // Function to fetch and parse CSV data using Papa Parse
  async function fetchData() {
    return new Promise((resolve, reject) => {
      Papa.parse(SHEET_URL, {
        download: true,
        header: true,
        complete: function(results) {
          if (results.errors.length > 0) {
            console.error("Papa Parse errors:", results.errors);
            reject(results.errors);
          } else {
            resolve(results.data);
          }
        },
        error: function(error) {
          console.error("Papa Parse error:", error);
          reject(error);
        }
      });
    });
  }

  // Function to process data (similar to your pandas operations)
  async function processData() {
    try {
      const rawData = await fetchData();

      // Rename columns
      const responses = rawData.map(item => ({
        Timestamp: item['Timestamp'],
        Gender: item['Jenis Kelamin'],
        Kampus: item['Asal Kampus'],
        Agen: item['Nama Lengkap Agen Pojok Statistik']
      }));

      const totalResponden = responses.length;
      const totalLaki = responses.filter(r => r.Gender === 'Laki-laki').length;
      const totalPerempuan = responses.filter(r => r.Gender === 'Perempuan').length;

      // Daily Progress
      const dailyProgressData = {};
      responses.forEach(r => {
        const date = r.Timestamp.split('T')[0]; // Extract date
        dailyProgressData[date] = (dailyProgressData[date] || 0) + 1;
      });

      const dailyProgress = Object.entries(dailyProgressData).map(([date, count]) => ({ x: date, y: count }));

      // Per Postat
      const perPostatData = {};
      responses.forEach(r => {
        perPostatData[r.Kampus] = (perPostatData[r.Kampus] || 0) + 1;
      });

      const perPostat = Object.entries(perPostatData).map(([kampus, count]) => ({ label: kampus, value: count }));

      // Rekap Kampus
      const rekapKampusData = {};
      responses.forEach(r => {
        rekapKampusData[r.Kampus] = (rekapKampusData[r.Kampus] || 0) + 1;
      });

      // Rekap Agen
      const rekapAgenData = {};
      responses.forEach(r => {
        const key = `${r.Kampus}-${r.Agen}`;
        rekapAgenData[key] = (rekapAgenData[key] || 0) + 1;
      });

      const rekapAgen = Object.entries(rekapAgenData).map(([key, count]) => {
        const [kampus, agen] = key.split('-');
        return { kampus, agen, value: count };
      });

      return {
        totalResponden,
        totalLaki,
        totalPerempuan,
        dailyProgress,
        perPostat,
        rekapKampusData,
        rekapAgen
      };
    } catch (error) {
      console.error("Error processing data:", error);
      alert("Error processing data. Check console for details.");
      return null;
    }
  }

  // Function to render the charts and update the DOM
  async function renderData() {
    const processedData = await processData();

    if (!processedData) {
      return; // Or handle the error if data processing failed
    }

    // Update Metrics
    document.getElementById('total-responden').textContent = processedData.totalResponden;
    document.getElementById('total-laki').textContent = processedData.totalLaki;
    document.getElementById('total-perempuan').textContent = processedData.totalPerempuan;

    // Render Daily Progress Chart
    renderDailyProgressChart(processedData.dailyProgress);

    // Render Per Postat Chart
    renderPerPostatChart(processedData.perPostat);

    // Update Kampus Data
    document.getElementById('unpad-count').textContent = processedData.rekapKampusData['Universitas Padjadjaran'] || 0;
    document.getElementById('unpar-count').textContent = processedData.rekapKampusData['Universitas Katolik Parahyangan'] || 0;
    document.getElementById('ipb-count').textContent = processedData.rekapKampusData['Institut Pertanian Bogor'] || 0;
    document.getElementById('ui-count').textContent = processedData.rekapKampusData['Universitas Indonesia'] || 0;
    document.getElementById('unisba-count').textContent = processedData.rekapKampusData['Universitas Islam Bandung'] || 0;
    document.getElementById('unsil-count').textContent = processedData.rekapKampusData['Universitas Siliwangi'] || 0;
    document.getElementById('upb-count').textContent = processedData.rekapKampusData['Universitas Pelita Bangsa'] || 0;

    // Render Monev Batang Chart
    renderMonevBatangChart(processedData.rekapAgen);

    // Render Monev Trimep Chart
    renderMonevTrimepChart(processedData.rekapAgen);
  }

  // ApexCharts rendering functions
  function renderDailyProgressChart(data) {
    const options = {
      chart: { type: 'bar', height: 300 },
      series: [{ name: 'Responden', data: data }],
      xaxis: { type: 'datetime' },
      yaxis: { title: { text: 'Jumlah Responden' } },
      colors: [getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim()]
    };
    const chart = new ApexCharts(document.querySelector("#progres-harian"), options);
    window.dailyProgressChart = chart;
    chart.render();
  }

  function renderPerPostatChart(data) {
    const options = {
      chart: { type: 'pie', height: 300 },
      series: data.map(item => item.value),
      labels: data.map(item => item.label),
      legend: { position: 'bottom' },
      colors: [getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim()]
    };
    const chart = new ApexCharts(document.querySelector("#per-postat"), options);
    chart.render();
  }

  function renderMonevBatangChart(data) {
    const options = {
      chart: { type: 'bar', height: 400 },
      series: [{ name: 'Responden', data: data.map(item => item.value) }],
      xaxis: { categories: data.map(item => item.agen) },
      yaxis: { title: { text: 'Jumlah Responden' } },
      colors: [getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim()]
    };

    const chart = new ApexCharts(document.querySelector("#monev-batang"), options);
    chart.render();
  }

  function renderMonevTrimepChart(data) {
    // Struktur ulang data untuk hierarki
    const kampusData = {};
    data.forEach(item => {
        if (!kampusData[item.kampus]) {
            kampusData[item.kampus] = {
                name: item.kampus,
                children: []
            };
        }
        kampusData[item.kampus].children.push({
            name: item.agen,
            value: item.value
        });
    });

    const seriesData = Object.values(kampusData).map(kampus => ({
        data: [{
            x: kampus.name,
            y: 1, // Nilai dummy, treemap akan menggunakan children
            children: kampus.children
        }]
    }));

    const options = {
        series: seriesData,
        chart: {
            height: 350,
            type: 'treemap'
        },
        legend: {
            show: false
        },
        // Tambahkan opsi untuk kendali tampilan
        plotOptions: {
            treemap: {
                distributed: true,
                enableShades: true
            }
        }
    };

    const chart = new ApexCharts(document.querySelector("#monev-trimep"), options);
    chart.render();
}

    function updateChartColors(theme) {
        let primaryColor;
        if (theme === 'blue') {
            primaryColor = '#0d6efd';
        } else if (theme === 'green') {
            primaryColor = '#28a745';
        } else {
            primaryColor = '#fd7e14';
        }

        // Update Daily Progress Chart options (example)
        dailyProgressChart.updateOptions({
            chart: {
                foreColor: primaryColor // change the title color
            },
            xaxis: {
              labels: {
                style: {
                  colors: primaryColor,
                }
              }
            },
            yaxis: {
              labels: {
                style: {
                  colors: primaryColor,
                }
              }
            }

        });

        // Update other charts similarly
    }

  // Initial Data Load and Rendering
  renderData();

});