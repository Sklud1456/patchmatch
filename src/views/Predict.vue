<template>
	<section>
    <el-row>
      <el-col :span="24"><div class="grid-content1 bg-purple-dark" font-family="Helvetica Neue">
        <h1 class="title">&nbsp Predict Page</h1>
      </div>
      </el-col>
    </el-row>
    <el-container>
        <el-row :gutter="10">
          <el-col :span="11" :offset="1">
            <div class="grid-content bg-purple">
              <b data="CVE_detial" class="cvetitle">{{cve}}<br></b>
              <div class="grid-content bg-blue-light">
                <a data="CVE_detial" class="cvedetial1">Warehouse Name:</a>
                <a data="CVE_detial" class="cvedetial2">{{CVE_detial.repo_name}}<br></a>
              </div>
              <div class="grid-content bg-blue-dark">
                <a data="CVE_detial" class="cvedetial1">Disclose Time:</a>
                <a data="CVE_detial" class="cvedetial2">{{CVE_detial.cvetime}}<br></a>
              </div>
              <div class="grid-content bg-blue-light">
                <a data="CVE_detial" class="cvedetial1">description:</a>
                <a data="CVE_detial" class="cvedetial2">{{CVE_detial.Description}}<br></a>
              </div>
              <div class="grid-content bg-blue-dark">
                <a data="CVE_detial" class="cvedetial1">Risk Score:</a>
                <a data="CVE_detial" class="cvedetial2">{{CVE_detial.score}}  </a>
                <el-tag class="tag" effect="dark" :color=tagcolor>{{CVE_detial.S_des}}</el-tag>
              </div>
              <div class="grid-content bg-blue-light">
                <a data="CVE_detial" class="cvedetial1">CWE:</a>
                <a data="CVE_detial" class="cvedetial2">{{CVE_detial.cwe_id}}    </a>
                <a data="CVE_detial" class="cvedetial2"> {{CVE_detial.cwe_name}}<br></a>
              </div>
              <div class="grid-content bg-blue-dark">
                <a data="CVE_detial" class="cvedetial1">COMMIT:</a>
                <a data="CVE_detial" class="cvedetial2">{{CVE_detial.patch_gitcommit}}</a>
                <el-button size="small" @click="getRank()">Predict</el-button>
                <!-- <el-button size="small" @click="test()">test</el-button> -->
              </div>
              <div id="kuuga" class="grid-content bg-blue-light-fortopn">
                <a data="CVE_detial" class="cvedetial1">TopN:</a>
                <template>
                  <el-radio v-model="radio" label=5>5</el-radio>
                  <el-radio v-model="radio" label=10>10</el-radio>
                  <el-radio v-model="radio" label=15>15</el-radio>
                  <el-radio v-model="radio" label=20>20</el-radio>
                  <el-button size="small" @click="topN()">OK</el-button>
                </template>
              </div>
            </div>
          </el-col>
        
          <el-col :span="11" aria-disabled="false">
            <div class="grid-content bg-purple" overflow:hidden>
              <el-table :data="commitlist"  highlight-current-row border-collapse v-loading="listLoading" style="width: 100%;">
                <el-table-column prop="commit_id" label="Commit ID" width="220">
                </el-table-column>
                <el-table-column prop="repo_name" label="Warehouse Name" width="120" >
                </el-table-column>
                <el-table-column prop="prob" label="Predict Score" width="140" >
                </el-table-column>
                <el-table-column prop="rank" label="Rank" width="80">
                </el-table-column>
                <el-table-column label="Operation" width="160">
                  <template scope="scope">
                    <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Detials</el-button>
                    <el-button type="primary" size="small" @click="chooseit(scope.$index, scope.row.commit_id)">Check</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-col>
        </el-row>
    </el-container>
    <!--详情界面-->
		<el-dialog title="Detials" :visible.sync="detailFormVisible" :close-on-click-modal="false">
			<el-form :model="detailForm" label-width="80px" :rules="detailFormRules" ref="detailForm">
        <el-form-item label="commit_id" prop="commit_id">
					<el-input v-model="detailForm.commit_id" auto-complete="off"></el-input>
				</el-form-item>
				<el-row>
          <el-col :span="12">
            <el-form-item label="Warehouse Name">
            <el-input v-model="detailForm.repo_name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Author">
            <el-input v-model="detailForm.author"></el-input>
            </el-form-item>
          </el-col>
				</el-row>
				<el-row>
          <el-col :span="30">
            <el-form-item label="Commit Time">
            <el-input v-model="detailForm.commit_time" auto-complete="off"></el-input>
          </el-form-item>
          </el-col>
				</el-row>
				<el-form-item label="description">
					<el-input type="textarea" v-model="detailForm.description"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="detailFormVisible = false">Back</el-button>
			</div>
		</el-dialog>

    <el-dialog title="Reminder" :visible.sync="checktocommitOK" width="30%">
      <span>Update successed</span>
      <span slot="footer" class="dialog-footer">
        <!-- <el-button @click="checktocommitOK = false">取 消</el-button> -->
        <el-button type="primary" @click="back()">OK</el-button>
      </span>
    </el-dialog>

    <el-dialog title="Reminder" :visible.sync="checktocommitNG" width="30%">
      <span>Update Error</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="checktocommitNG = false">Back</el-button>
        <el-button type="primary" @click="checktocommitNG = false">OK</el-button>
      </span>
    </el-dialog>

    <el-dialog title="Reminder" :visible.sync="ask" width="30%">
      <span>Confirm that the COMMIT is selected as the CVE patch?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="ask = false">Back</el-button>
        <el-button type="primary" @click="checkit()">OK</el-button>
      </span>
    </el-dialog>

	</section>
</template>


<script>
import util from "../common/js/util";
import {getSignalCVE, getPredictRank, CheckCommit} from "../api/api";

export default {
  data() {
    return {
      radio:10,
      cve:this.$route.params.datacve,
      Commit_id:"",
      CVE_detial:{},
      commitlist:[],
      commitlist1:[],
      tagcolor:"",
      listLoading: false,
      detailFormVisible: false,
      checktocommitOK: false,
      checktocommitNG: false,
      ask:false,
      detailForm: {},
      detailFormRules: {
        name: [{ required: true, message: "请输入姓名", trigger: "blur" }]
      },
      checkcode: 0,
      checkmsg: "",
    };
  },
  methods: {
    // handleCurrentChange(val) {
    //   this.page = val;
    //   this.getUsers();
    // },
    //获取CVE具体信息
    back(){
      this.checktocommitOK = false
      this.$router.push({  
          path: '/CVEtable', 
          component: './views/nav1/CVETable.vue', 
          name: 'CVE List' 
        })
    },
    getCVEdetial() {
      let para = {
        CVE: this.cve,
      };
      getSignalCVE(para).then(res => {
        console.log("1:"+res.data.code)
        this.CVE_detial = res.data.CVEinfos;
        this.cve=res.data.cve;
        var a=res.data.color;
        if(a=='CRITICAL'){
          this.tagcolor="#FF6E76"
        }
        else if(a=='HIGH'){
          this.tagcolor="#FDDD60"
        }
        else if(a=='MEDIUM'){
          this.tagcolor="#58D9F9"
        }
        else if(a=='LOW'){
          this.tagcolor="#7CFFB2"
        }
        else if(a=='NONE'){
          this.tagcolor="#808080"
        }
      });

    },
    topN(){
      console.log(this.radio)
      this.commitlist=this.commitlist1.slice(0,this.radio)
    },
    test() {
      console.log("1111")
      // document.getElementById("kuuga").style.display="block";
      console.log(this.radio)
    },
    //获得commit对应排名
    getRank() {
      let para = {
        CVE: this.cve,
      };
      var i;
      this.listLoading = true;
      getPredictRank(para).then(res => {
        console.log("2:"+res.data.code)
        // this.commitlist = res.data.commitlist;
        this.commitlist1 = res.data.commitlist;
        this.commitlist=this.commitlist1.slice(0,10)
        this.listLoading = false;
        document.getElementById("kuuga").style.display="block";
      });
    },
    //显示详情界面
    handleEdit: function(index, row) {
      this.detailFormVisible = true;
      this.detailForm = Object.assign({}, row);
    },
    chooseit: function(index, row) {
      this.Commit_id=row;
      this.ask=true;
    },
    checkit: function() {
      let para={
        Commit_id: this.Commit_id,
        CVE_id: this.cve,
      }
      CheckCommit(para).then(res => {
        this.checkcode = res.data.code;
        console.log("code:"+this.checkcode)
        this.checkmsg = res.data.msg;
      });
      console.log(this.checkcode)
      if(this.checkcode==500){
        this.checktocommitNG=true;
      }
      else{
        this.checktocommitOK=true;
      }
      this.getCVEdetial();
      this.ask=false
    },
    selsChange: function(sels) {
      this.sels = sels;
    },
  },
  mounted() {
    this.getCVEdetial();
    // console.log("2:"+CVE_detial.repo_name)
    // console.log("3:"+CVE_detial.cvetime)
  }
};
</script>

<style>
  .el-row {
    margin-bottom: 20px;
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  
  .bg-blue-light {
    background: #b3ffff;
  }
  .bg-blue-light-fortopn {
    background: #b3ffff;
    display: none;
  }
  .bg-blue-dark {
    background: #00e5e6;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 10px;
    min-height: 40px;
  }
  .grid-content1 {
    min-height: 40px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .title {
    font-family: "微软雅黑";
    float: medium;
    color: #ffffff;
  }
  .cvetitle {
    font-family: "PingFang SC";
    font-size: 30px;
    float: medium;
    color: #000000;
  }
  .cvedetial1 {
    font-family: "PingFang SC";
    font-size: 23px;
    float: medium;
    color: #000000;
  }
  .cvedetial2 {
    font-family: "PingFang SC";
    font-size: 20px;
    float: medium;
    color: #000000;
  }
  .tag {
    font-family: "PingFang SC";
    font-size: 20px;
    float: medium;
    color: #ffffff;
  }
</style>