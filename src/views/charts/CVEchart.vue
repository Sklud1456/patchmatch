<template>
    <section class="chart-container">
        <el-row>
            <el-col :span="14">
                <el-table :data="tableData" style="width: 100%" max-height="400" :default-sort = "{prop: 'date', order: 'descending'}">
                  <el-table-column prop="CVE_id" label="CVE-ID" sortable width="110">
                  </el-table-column>
                  <el-table-column prop="repo_name" label="Warehouse Name" sortable width="120">
                  </el-table-column>
                  <el-table-column prop="cwe_name" label="CWE" width="220">
                  </el-table-column>
                  <el-table-column prop="score" label="Risk Score" width="120">
                  </el-table-column>
                  <el-table-column prop="cvetime" label="Time" width="120">
                  </el-table-column>
                </el-table>
            </el-col>
            <el-col :span="10">
                <div id="chartWatch" style="width:100%; height:400px;"></div>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="12">
                <div id="chartCircle" style="width:100%; height:500px;"></div>
            </el-col>
            <el-col :span="12">
                <div id="chartPie" style="width:100%; height:500px;"></div>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="24">
                <div id="chartLine" style="width:100%; height:300px;"></div>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="24">
                <div id="chartSquare" style="width:100%; height:300px;"></div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
import echarts from "echarts";
import { getCVEPieChart, getCVELineChart,getCVEWatchChart,getCVECircleChart,getCVESquareChart,getNewCVEs } from "../../api/api";
export default {
  data() {
    return {
      chartLine: null,
      chartPie: null,
      chartwatch: null,
      chartCircle: null,
      chartSquare: null,
      tableData: []  
    }
  },

  methods: {
    formatter(row, column) {
        return row.address;
    },
    drawPieChart() {
      this.chartPie = echarts.init(document.getElementById("chartPie"));
      getCVEPieChart().then(res => {
        let { value, code, total,repo } = res.data;
        console.log(repo)
        console.log(value)
        var temp=new Array()
        var i=0;
        for(i=0;i<value.length;i++){
          temp[i]={value:value[i].num,name:value[i].repo_name}
        }
        console.log(temp)
        if (code !== 200) {
          this.$message({
            message: "服务端发生错误",
            type: "warning"
          });
        } else {
          this.chartPie.setOption({
            title: {
              text: "The Number of CVE per Warehouse",
              subtext: "Total Number:" + total,
              x: "center"
            },
            tooltip: {
              trigger: "item",
              formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
              orient: "vertical",
              left: "left",
              data: repo// 和value一一对应
            },
            toolbox: {
              show: true,
              feature: {
                saveAsImage: { show: true }
              }
            },
            series: [
              {
                name: "proportion",
                type: "pie",
                radius: "55%",
                center: ["50%", "60%"],
                data: temp,
                itemStyle: {
                  emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: "rgba(0, 0, 0, 0.5)"
                  }
                }
              }
            ]
          });
        }
      });
    },
    drawLineChart() {
      this.chartLine = echarts.init(document.getElementById("chartLine"));
      getCVELineChart().then(res => {
        let { value, total, time, code } = res.data;
        if (code !== 200) {
          this.$message({
            message: "服务端发生错误",
            type: "warning"
          });
        } else {
          this.chartLine.setOption({
            //源自用电量分布
            title: {
              text: 'Distribution of CVE Time',
              subtext: 'The Number of CVE per Year'
            },
            tooltip: {
              trigger: 'axis',
              axisPointer: {
              type: 'cross'
              }
            },
            // legend: {
            //   data: grade_value
            // },
            toolbox: {
              show: true,
              feature: {
                // magicType: { show: true, type: ["line", "bar"] },
                // saveAsImage: { show: true }
                saveAsImage: {show:true}
              }
            },
            // calculable: true,
            xAxis: {
              type: "category",
              boundaryGap: false,
              // prettier-ignore
              data: time
            },
            yAxis: {
              type: 'value',
              axisLabel: {
                formatter: '{value}'
              },
              axisPointer: {
                snap: true
              }
            },
              series: [
              {
                name: 'number',
                type: 'line',
                smooth: false,
                itemStyle: {
                  normal: {
                  color:"#3F77FE",
                  //常见颜色：#FFD700 亮黄色，#3F77FE 蓝色
                  },
                },
                // prettier-ignore
                data: value
              }
            ],
          });
        }
      });
    },
    drawWatchChart() {
      this.chartWatch = echarts.init(document.getElementById("chartWatch"));
      getCVEWatchChart().then(res => {
        let { score,num, code } = res.data;
        if (code !== 200) {
          this.$message({
            message: "服务端发生错误",
            type: "warning"
          });
        } else {
          this.chartWatch.setOption({
            //源自等级仪表盘
            title: {
              top:"-1px",
              text: 'The degree of risk',
              subtext: 'Risk score of CVE,the number of effective:'+num
            },
            toolbox: {
              show: true,
              feature: {
                saveAsImage: { show: true }
              }
            },
            series: [
            {
              center:["50%","70%"],//调整仪表盘位置
              type: 'gauge',
              startAngle: 180,
              endAngle: 0,
              min: 0,
              max: 10,
              splitNumber: 16,
              axisLine: {
                lineStyle: {
                  width: 6,
                  color: [
                    [0.25, '#7CFFB2'],
                    [0.5, '#58D9F9'],
                    [0.75, '#FDDD60'],
                    [1, '#FF6E76']
                  ]
                }
              },
              pointer: {//指针
                icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                length: '60%',
                width: 10,
                offsetCenter: [0, "-60%"],
                itemStyle: {
                  color: 'auto'
                }
              },
              axisTick: {
                length: 12,
                lineStyle: {
                  color: 'auto',
                  width: 2
                }
              },
              splitLine: {
                length: 20,
                lineStyle: {
                  color: 'auto',
                  width: 4
                }
              },
              axisLabel: {//仪表盘数据
                color: '#464646',
                fontSize: 15,
                distance: -90,
                formatter: function (value) {
                  if (value === 9.375) {
                    return 'CRITICAL';
                  } else if (value === 7.5) {
                    return 'HIGH';
                  } else if (value === 2.5) {
                    return 'MEDIUM';
                  } else if (value === 0.625) {
                    return 'LOW';
                  }
                  return '';
                }
              },
              
              title: {
                offsetCenter: [0, '-20%'],
                fontSize: 30
              },
              detail: {
                fontSize: 40,
                offsetCenter: [0, '30%'],
                valueAnimation: true,
                formatter: function (value) {
                  return "AVG Risk Score:"+value;
                },
                color: 'auto',
              },
              data: [
                {
                  offsetCenter: [0, '50%'],
                  fontSize: 10,
                  value: score,
                  num: num,
                }
              ]
            }
            ]
          });
        }
      });
    },
    drawCircleChart() {
      this.chartCircle = echarts.init(document.getElementById("chartCircle"));
      getCVECircleChart().then(res => {
        let { total, value, code,name } = res.data;
        if (code !== 200) {
          this.$message({
            message: "服务端发生错误",
            type: "warning"
          });
        } else {
          this.chartCircle.setOption({
            //源自圆角环形，圆角似乎无法渲染
            color:['#FF6E76','#FDDD60','#58D9F9','#7CFFB2','#808080'],//红，黄，蓝，绿，灰
            title: {
              text: 'Distribution of Risk Score',
              subtext: 'Counts The CVE Risk Score'
            },
            toolbox: {
              show: true,
              feature: {
                saveAsImage: { show: true }
              }
            },
            tooltip: {
              trigger: 'item'
            },
            legend: {
              orient: "vertical",
              left: "left",
              bottom:"1%",
              data: name// 和value一一对应
            },
            series: [
              {
                name: 'risk score',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: true,
                itemStyle: {
                  borderRadius: 10,
                  borderColor: '#fff',
                  borderWidth: 2
                },
                label: {
                  show: true,
                  position: 'left'
                },
                emphasis: {
                  label: {
                    show: false,
                    fontSize: '40',
                    fontWeight: 'bold'
                  }
                },
                labelLine: {
                  show: false
                },
                data: value,
              }
            ]
          });
        }
      });
    },
    drawSquareChart() {
      this.chartSquare = echarts.init(document.getElementById("chartSquare"));
      getCVESquareChart().then(res => {
        let { name,value,total,code } = res.data;
        if (code !== 200) {
          this.$message({
            message: "服务端发生错误",
            type: "warning"
          });
        } else {
          this.chartSquare.setOption({
            //源自柱形图
            toolbox: {
              show: true,
              feature: {
                saveAsImage: { show: true }
              }
            },
            axisLabel: {  
              interval: 0,  
              formatter:function(value)  
              {  
                  var ret ="";//拼接加\n返回的类目项  
                  var maxLength = 12;//每项显示文字个数  
                  var valLength = value.length;//X轴类目项的文字个数  
                  var rowN = Math.ceil(valLength / maxLength); //类目项需要换行的行数  
                  if (rowN > 1)//如果类目项的文字大于3,  
                  {  
                      for (var i = 0; i < rowN; i++) {  
                          var temp = "";//每次截取的字符串  
                          var start = i * maxLength;//开始截取的位置  
                          var end = start + maxLength;//结束截取的位置  
                          //这里也可以加一个是否是最后一行的判断，但是不加也没有影响，那就不加吧  
                          temp = value.substring(start, end) + "\n";  
                          ret += temp; //凭借最终的字符串  
                      }  
                      return ret;  
                  }  
                  else {  
                      return value;  
                  }  
              }  
            },  
            title: {
              text: 'Distribution of Risk Type',
              subtext: 'Classification of Risk Types According to CWE-name'
            },
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'shadow'
              }
            },
            grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
            },
            xAxis: [
              {
                type: 'category',
                data: name,
                axisTick: {
                  alignWithLabel: true
                }
              }
            ],
            yAxis: [
              {
                type: 'value'
              }
            ],
            series: [
              {
                name: 'Direct',
                type: 'bar',
                barWidth: '60%',
                data: value
              }
            ]
          });
        }
      });
    },
    getNewCVETable() {
      getNewCVEs().then(res => {
        this.tableData = res.data.CVEs;
      });
    },
    drawCharts() {
      // console.log(echarts.version)
      this.drawLineChart();
      this.drawPieChart();
      this.drawWatchChart();
      this.drawCircleChart();
      this.drawSquareChart();
      this.getNewCVETable();
    }
  },

  mounted: function() {
    this.drawCharts();
  },
  // updated: function() {
  //   this.drawCharts();
  // }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  float: left;
}
/*.chart div {
        height: 400px;
        float: left;
    }*/

.el-col {
  padding: 30px 20px;
}
</style>
