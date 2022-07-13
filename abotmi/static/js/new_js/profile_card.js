var bodyLoaded = document.body;
var m_d = document.querySelector('.UZ-profile-badge');
var data_batch = m_d.getAttribute('data-batch');
var ba_a_li = document.querySelector('.ba_a_l');
var c_d = document.createElement('div');
c_d.setAttribute('class', 'UZ-cd');
var c_b = document.createElement('div');
c_b.setAttribute('class', 'UZ_cd_bd');
var ch_dv = document.createElement('div');
var s_ch_dv = document.createElement('div');
var pr_pc = document.createElement('img');
pr_pc.setAttribute('class', 'img-response us-dp');
var ad_tit = document.createElement('h2');
ad_tit.setAttribute('class', 'tit');
var ad_lc = document.createElement('p');
ad_lc.setAttribute('class', 'lc');
var v_p_bt = document.createElement('a');
v_p_bt.setAttribute('class', 'btn pr-btn');
v_p_bt.innerHTML = 'View Profile';
v_p_bt.href = ba_a_li.href;
v_p_bt.setAttribute('target', '_blank');
var uz_c_l = document.createElement('img');
uz_c_l.setAttribute('class', 'img-response c_l');
uz_c_l.setAttribute('src', 'https://upwrdz.com/static/new_images/logo.png');
ch_dv.appendChild(pr_pc);
ch_dv.appendChild(ad_tit);
ch_dv.appendChild(ad_lc);
s_ch_dv.appendChild(v_p_bt);
s_ch_dv.appendChild(uz_c_l);
c_b.appendChild(ch_dv);
c_b.appendChild(s_ch_dv);
c_d.appendChild(c_b);
m_d.appendChild(c_d);
var n_sc = document.createElement('script');
n_sc.src = 'https://test.upwrdz.com/api/get_profile_card/?batch='+data_batch+'&callback=myCallbackFunction';
bodyLoaded.appendChild(n_sc);
var uz_st_li = document.createElement('link');
uz_st_li.href = 'https://test.upwrdz.com/static/css/batch_card.css';
uz_st_li.setAttribute('rel', "stylesheet");
bodyLoaded.appendChild(uz_st_li);
function myCallbackFunction(data){
    if(data != 'undefined'){
        ad_tit.innerHTML = data.tit;
        ad_lc.innerHTML = data.loc;
        pr_pc.src = data.pic;
        ba_a_li.style.display = 'none';
    }
}