# budget_word_problems.py
import uuid
import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("**📚 Year 5 > Financial Maths**")
    st.title("💵 Budget Word Problems")

    # Optional Back button (works with your query-param nav pattern)
    left, right = st.columns([1, 5])
    with left:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

    # Unique ID so multiple instances don’t collide
    app_id = f"budget-app-{uuid.uuid4().hex[:8]}"

    # NOTE: this is a *raw* string so JS template literals like ${...} are safe.
    # We only replace the placeholder token __APP_ID__ afterwards.
    html = r"""
    <style>
      .app-wrap {font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; max-width: 900px; margin: 0 auto}
      .row{display:flex; align-items:center; gap:12px; flex-wrap:wrap}
      .pill{display:inline-flex; align-items:center; gap:8px; padding:6px 10px; border-radius:999px; background:#f1f5f9; border:1px solid #e2e8f0; font-size:14px}
      .card{background:#f0f8ff; padding:18px; border-radius:12px; border-left:4px solid #4CAF50; margin:18px 0}
      .btn{padding:8px 14px; border-radius:8px; border:1px solid transparent; cursor:pointer; font-weight:600}
      .btn-primary{background:#1d4ed8; color:#fff}
      .btn-success{background:#22c55e; color:#fff}
      .btn-warning{background:#f59e0b; color:#111827}
      .btn-ghost{background:#fff; border-color:#cbd5e1}
      .muted{color:#475569; font-size:13px}
      .answer-box input{width:160px; padding:8px 10px; border-radius:8px; border:1px solid #cbd5e1; font-size:16px}
      .ok{color:#16a34a; font-weight:700}
      .bad{color:#b00020; font-weight:700}
      .panel{background:#fff3cd; border-left:4px solid #f59e0b; padding:14px; border-radius:8px; margin-top:10px}
      .list{line-height:1.8}
      .footer-note{margin-top:18px; font-size:13px; color:#64748b}
    </style>

    <div id="__APP_ID__" class="app-wrap">
      <div class="row" style="justify-content:space-between; margin:10px 0 4px;">
        <div class="row">
          <span class="pill">
            <strong>Difficulty</strong>
            <select id="__APP_ID__-diff" style="border:none; background:transparent; outline:none;">
              <option value="1" selected>Easy</option>
              <option value="2">Medium</option>
              <option value="3">Hard</option>
            </select>
          </span>
          <button id="__APP_ID__-new" class="btn btn-ghost">↻ New Problem</button>
        </div>
        <div class="muted">All amounts are dollars.</div>
      </div>

      <div id="__APP_ID__-q" class="card">Loading problem…</div>

      <div class="row answer-box" style="gap:10px;">
        <div class="row" style="gap:6px;">
          <span class="muted" style="font-weight:700;">$</span>
          <input id="__APP_ID__-ans" placeholder="Enter amount" />
        </div>
        <button id="__APP_ID__-submit" class="btn btn-success">Submit</button>
      </div>

      <div id="__APP_ID__-fb" style="margin-top:12px;"></div>

      <div class="footer-note">
        Tips: Read carefully, list each line (spend / save / donate / keep), then add them all.
        Tax/tip lines are already computed—just include them in the sum.
      </div>
    </div>

    <script>
    (function(){
      const APP="__APP_ID__";
      const male=new Set(["John","Mike","Tom","Ben","Alex","Ryan","David","Kevin","Oliver","Lucas","James","Ethan","Nathan","Daniel","Jake","Noah","Tyler","Jordan","Brandon","Mason","Logan"]);
      const byId=(s)=>document.getElementById(APP+s);
      const rint=(a,b)=>Math.floor(Math.random()*(b-a+1))+a;
      const pick=(arr)=>arr[Math.floor(Math.random()*arr.length)];
      const currency=(x)=>"$"+Number(x).toLocaleString(undefined,{minimumFractionDigits:(x%1?2:0),maximumFractionDigits:2});
      const he=(n)=>male.has(n)?"he":"she";
      const his=(n)=>male.has(n)?"his":"her";

      // ---------- Easy scenarios ----------
      function easyScenarios(){
        const A=['Maria','John','Sarah','Mike','Emma'],
              B=['Lisa','Tom','Amy','Ben'],
              C=['Alex','Sophie','Ryan','Zoe'],
              D=['Jake','Lily','Noah','Ella'];

        const giftCard=()=>{
          const person=pick(['Ava','Liam','Ella','Noah','Mia']);
          return {
            type:'gift_card',
            person,
            items:[
              {action:'spends', amount:rint(5,15), item:'headphones accessories'},
              {action:'spends', amount:rint(6,18), item:'stickers'},
              {action:'keeps',  amount:rint(3,10), item:'remaining balance'}
            ],
            opening: person+" has a gift card. "
          };
        };

        const schoolSupplies=()=>{
          const person=pick(['Jade','Owen','Ruby','Evan','Chloe']);
          return {
            type:'shopping',
            person,
            items:[
              {action:'buys', amount:rint(3,6), item:'notebooks'},
              {action:'buys', amount:rint(2,5), item:'pen pack'},
              {action:'buys', amount:rint(4,9), item:'art paper'}
            ],
            opening: person+" goes shopping for school supplies. "
          };
        };

        return [
          { type:'allowance', person:pick(A),
            items:[
              {action:'spends', amount:rint(3,8), item:'snacks'},
              {action:'saves',  amount:rint(5,10), item:'new toy'},
              {action:'keeps',  amount:rint(2,5),  item:'pocket money'}
            ]
          },
          { type:'birthday', person:pick(B),
            items:[
              {action:'buys',  amount:rint(10,20), item:'video game'},
              {action:'saves', amount:rint(15,25), item:'bicycle'},
              {action:'gives', amount:rint(5,10),  item:'sister'}
            ]
          },
          { type:'earnings', person:pick(C), job:pick(['lawn mowing','dog walking','car washing']),
            items:[
              {action:'spends', amount:rint(8,15),  item:'lunch'},
              {action:'saves',  amount:rint(20,30), item:'skateboard'}
            ]
          },
          { type:'chores', person:pick(D),
            items:[
              {action:'buys',    amount:rint(4,8),  item:'candy'},
              {action:'saves',   amount:rint(6,12), item:'book'},
              {action:'donates', amount:rint(2,5),  item:'charity'}
            ]
          },
          giftCard(),
          schoolSupplies()
        ];
      }

      // ---------- Medium scenarios ----------
      function mediumScenarios(){
        const N=['David','Rachel','Kevin','Julia','Oliver','Mia','Lucas','Ava',
                 'Tyler','Madison','Jordan','Ashley','Leo','Nora','Parker','Lila'];

        const movieNight=()=>{
          const person=pick(N), qty=rint(2,4), price=rint(9,12), snacks=rint(6,12);
          return {
            type:'event',
            person,
            items:[
              {action:'spends', amount:qty*price, item:`movie tickets (${qty} × $${price})`},
              {action:'spends', amount:snacks,     item:'snacks'}
            ],
            opening: person+" plans a movie night. "
          };
        };

        const classParty=()=>{
          const person=pick(N);
          return {
            type:'party',
            person,
            items:[
              {action:'budgets', amount:rint(12,20), item:'decorations'},
              {action:'budgets', amount:rint(18,30), item:'snacks'},
              {action:'budgets', amount:rint(10,18), item:'drinks'},
              {action:'budgets', amount:rint(8,16),  item:'prizes'}
            ],
            opening: person+" is organizing a classroom party. "
          };
        };

        return [
          { type:'monthly_budget', person:pick(N),
            items:[
              {action:'pays',   amount:rint(25,40), item:'phone bill'},
              {action:'spends', amount:rint(30,50), item:'groceries'},
              {action:'saves',  amount:rint(40,60), item:'vacation'},
              {action:'donates',amount:rint(10,20), item:'charity'}
            ]
          },
          { type:'part_time', person:pick(N), job:pick(['tutoring','babysitting','retail work']),
            items:[
              {action:'spends', amount:rint(15,25), item:'transportation'},
              {action:'saves',  amount:rint(50,80), item:'college'},
              {action:'spends', amount:rint(20,35), item:'entertainment'},
              {action:'gives',  amount:rint(15,25), item:'parents'}
            ]
          },
          { type:'summer_job', person:pick(N), job:pick(['camp counselor','lifeguard','ice cream shop']),
            items:[
              {action:'saves',  amount:rint(60,90), item:'laptop'},
              {action:'spends', amount:rint(25,40), item:'clothes'},
              {action:'spends', amount:rint(15,25), item:'movies'},
              {action:'keeps',  amount:rint(20,30), item:'spending money'}
            ]
          },
          movieNight(),
          classParty(),
          { type:'pet', person:pick(N),
            items:[
              {action:'spends', amount:rint(20,35), item:'pet supplies'},
              {action:'pays',   amount:rint(30,50), item:'adoption fee'},
              {action:'budgets',amount:rint(25,40), item:'first vet visit'}
            ],
            opening: "This person plans to adopt a pet. "
          }
        ];
      }

      // ---------- Hard scenarios ----------
      function hardScenarios(){
        const N=['Nathan','Grace','Daniel','Sophia','Brandon','Chloe','Mason',
                 'Harper','Logan','Emily','Ryan','Olivia','Dylan','Isla','Marco','Priya'];

        const dinnerWithTip=()=>{
          const person=pick(N), meals=rint(45,75),
                taxRate=pick([0.06,0.07,0.08]), tipRate=pick([0.15,0.18,0.2]);
          const tax=+(meals*taxRate).toFixed(2), tip=+(meals*tipRate).toFixed(2);
          return {
            type:'dinner',
            person,
            items:[
              {action:'pays', amount:meals, item:'meals'},
              {action:'pays', amount:tax,   item:`sales tax (~${Math.round(100*tax/meals)}%)`},
              {action:'pays', amount:tip,   item:`tip (~${Math.round(100*tip/meals)}%)`}
            ],
            opening: person+" pays for a family dinner. "
          };
        };

        const moving=()=>{
          const person=pick(N);
          return {
            type:'moving',
            person,
            items:[
              {action:'pays', amount:rint(60,110), item:'truck rental'},
              {action:'pays', amount:rint(20,45),  item:'fuel'},
              {action:'buys', amount:rint(18,32),  item:'boxes'},
              {action:'buys', amount:rint(6,12),   item:'tape'}
            ],
            opening: person+" is budgeting for moving. "
          };
        };

        const sports=()=>{
          const person=pick(N);
          return {
            type:'sports',
            person,
            items:[
              {action:'pays',  amount:rint(55,85), item:'registration fee'},
              {action:'pays',  amount:rint(35,60), item:'uniform'},
              {action:'buys',  amount:rint(25,45), item:'equipment'},
              {action:'keeps', amount:rint(10,20), item:'team snacks'}
            ],
            opening: person+" is joining a local sports team. "
          };
        };

        return [
          { type:'complex', person:pick(N),
            items:[
              {action:'pays',   amount:rint(45,65), item:'car payment'},
              {action:'saves',  amount:rint(80,120),item:'house'},
              {action:'spends', amount:rint(30,50), item:'food'},
              {action:'donates',amount:rint(20,30), item:'church'},
              {action:'keeps',  amount:rint(40,60), item:'personal use'}
            ]
          },
          { type:'business', person:pick(N), business:pick(['online store','lawn service','tutoring service']),
            items:[
              {action:'reinvests', amount:rint(100,150), item:'business'},
              {action:'saves',     amount:rint(75,125),  item:'taxes'},
              {action:'pays',      amount:rint(50,80),   item:'supplies'},
              {action:'keeps',     amount:rint(60,90),   item:'profit'}
            ]
          },
          { type:'travel', person:pick(N),
            items:[
              {action:'spends',   amount:rint(120,180), item:'hotel'},
              {action:'budgets',  amount:rint(80,120),  item:'food'},
              {action:'reserves', amount:rint(60,90),   item:'activities'},
              {action:'sets aside', amount:rint(40,60), item:'souvenirs'},
              {action:'keeps',    amount:rint(30,50),   item:'emergency fund'}
            ]
          },
          dinnerWithTip(),
          moving(),
          sports(),
          { type:'fundraiser', person:pick(N),
            items:[
              {action:'pays',  amount:rint(40,70), item:'booth fee'},
              {action:'buys',  amount:rint(30,55), item:'ingredients'},
              {action:'buys',  amount:rint(12,20), item:'packaging'},
              {action:'keeps', amount:rint(15,25), item:'change float'}
            ],
            opening: pick(['The class','The club'])+" led by "+pick(N)+" is starting a fundraiser. "
          }
        ];
      }

      function generateProblem(level){
        const pool=(level==1)?easyScenarios():(level==2)?mediumScenarios():hardScenarios();
        const sc=JSON.parse(JSON.stringify(pick(pool)));
        sc.total=Math.round(sc.items.reduce((s,it)=>s+Number(it.amount),0)*100)/100;
        return sc;
      }

      function formatProblem(sc){
        const person=sc.person, subj=he(person), poss=his(person);
        let text=sc.opening||"";
        if(!text){
          const map={
            'allowance': person+" receives a weekly allowance. Each week, ",
            'birthday':  person+" received birthday money. ",
            'earnings':  person+" earns money from "+(sc.job||"work")+". Each week, ",
            'chores':    person+" earns money doing chores. This week, ",
            'monthly_budget': person+" has a monthly budget. Each month, ",
            'part_time': person+" works part-time "+(sc.job||"")+". From the weekly earnings, ",
            'summer_job':person+" works as a "+(sc.job||"")+" during summer. Each week, ",
            'business':  person+" runs a small "+(sc.business||"business")+". From this week's earnings, ",
            'travel':    person+" is planning a trip. For the travel budget, ",
            'complex':   person+" manages a weekly budget. "
          }; text=map[sc.type]||person+" is planning a budget. ";
        }
        const lines=sc.items.map(it=>{
          const a=it.action, amt=currency(it.amount), item=it.item;
          if(a==='gives'&&item.includes('sister')) return subj+" gives "+amt+" to "+poss+" sister";
          if(a==='gives'&&item.includes('parents'))return subj+" gives "+amt+" to parents";
          if(['keeps','reserves','sets aside','budgets'].includes(a)) return subj+" "+a+" "+amt+" for "+item;
          if(a==='reinvests') return subj+" reinvests "+amt+" in the "+item;
          const prep=(a==='spends'||a==='buys')?" on ":" ";
          return (subj+" "+a+" "+amt+prep+item).trim();
        });
        if(lines.length===1) text+=lines[0]+".";
        else if(lines.length===2) text+=lines[0]+" and "+lines[1]+".";
        else text+=lines.slice(0,-1).join(", ")+", and "+lines.slice(-1)[0]+".";
        const q={
          'allowance': "\n\nHow much is "+person+"'s weekly allowance?",
          'birthday':  "\n\nHow much birthday money did "+person+" receive?",
          'earnings':  "\n\nHow much does "+person+" earn from "+(sc.job||"work")+" each week?",
          'chores':    "\n\nHow much did "+person+" earn from chores this week?",
          'monthly_budget': "\n\nWhat is "+person+"'s total monthly budget?",
          'part_time': "\n\nHow much does "+person+" earn weekly from "+(sc.job||"work")+"?",
          'summer_job':"\n\nWhat is "+person+"'s weekly earnings as a "+(sc.job||"worker")+"?",
          'business':  "\n\nWhat were "+person+"'s total earnings from the "+(sc.business||"business")+" this week?",
          'travel':    "\n\nWhat is "+person+"'s total travel budget?",
          'gift_card': "\n\nWhat was the original value of "+person+"'s gift card?",
          'shopping':  "\n\nWhat is the total amount spent?",
          'event':     "\n\nWhat is the total cost of the night out?",
          'party':     "\n\nWhat is the total party budget?",
          'pet':       "\n\nWhat is the total cost to get the pet?",
          'dinner':    "\n\nWhat is the total bill?",
          'moving':    "\n\nWhat is the total moving cost?",
          'sports':    "\n\nWhat is the total amount "+person+" needs?",
          'fundraiser':"\n\nWhat are the total kickoff costs?",
          'complex':   "\n\nWhat is "+person+"'s total weekly budget?"
        }[sc.type]||"\n\nWhat is the total amount?";
        return text+q;
      }

      function solutionHTML(sc){
        const list=sc.items.map(it=>`<li>${it.action.charAt(0).toUpperCase()+it.action.slice(1)} for ${it.item}: <b>${currency(it.amount)}</b></li>`).join("");
        const sum=sc.items.map(it=>currency(it.amount)).join(" + ");
        return `<div class="panel"><h4 style="margin:0 0 6px;">Step-by-Step Solution</h4>
          <ol class="list" style="margin:6px 0;">
            <li><b>List all amounts:</b><ul>${list}</ul></li>
            <li><b>Add them:</b> ${sum} = <b>${currency(sc.total)}</b></li>
            <li><b>Answer:</b> ${currency(sc.total)}</li>
          </ol></div>`;
      }

      const elQ=document.getElementById(APP+"-q"),
            elAns=document.getElementById(APP+"-ans"),
            elFB=document.getElementById(APP+"-fb"),
            elDiff=document.getElementById(APP+"-diff"),
            elNew=document.getElementById(APP+"-new"),
            elSubmit=document.getElementById(APP+"-submit");

      let state={level:1, problem:null, locked:false};

      function renderProblem(){
        state.problem=generateProblem(state.level);
        elQ.innerHTML='<div class="card"><p style="white-space:pre-wrap;">'+formatProblem(state.problem)+'</p></div>';
        elFB.textContent="";
        elAns.value="";
        elAns.disabled=false;
        state.locked=false;
        elAns.focus();
      }

      function submit(){
        if(state.locked) return;
        const raw=(elAns.value||"").replace(/\$/g,"").replace(/,/g,"").trim();
        const val=Number(raw);
        if(!isFinite(val)){
          elFB.innerHTML="<div class='bad'>Please enter a valid number.</div>";
          return;
        }
        state.locked=true; elAns.disabled=true;
        const correct=state.problem.total;

        if(Math.abs(val-correct)<0.01){
          elFB.innerHTML="<div class='ok'>✅ Correct! The answer is <b>"+currency(correct)+"</b>.</div>";
        }else{
          elFB.innerHTML="<div class='bad' style='margin-bottom:6px;'>❌ Incorrect. Your answer: <b>"+currency(val)+"</b></div>"
                        +"<button id='__APP_ID__-show' class='btn btn-warning'>Show solution</button>"
                        +"<div id='__APP_ID__-sol'></div>";
          document.getElementById(APP+"-show").onclick=()=>{
            document.getElementById(APP+"-sol").innerHTML=solutionHTML(state.problem);
            document.getElementById(APP+"-show").disabled=true;
          };
        }
        const next=document.createElement('button');
        next.className="btn btn-primary"; next.textContent="Next Problem"; next.style.marginTop="8px";
        next.onclick=renderProblem; elFB.appendChild(document.createElement('br')); elFB.appendChild(next);
      }

      elDiff.onchange=(e)=>{ state.level=Number(e.target.value); renderProblem(); };
      elNew.onclick=renderProblem;
      elSubmit.onclick=submit;
      elAns.addEventListener('keydown',(ev)=>{ if(ev.key==='Enter') submit(); });

      renderProblem();
    })();
    </script>
    """

    # Inject the unique ID
    html = html.replace("__APP_ID__", app_id)

    # Render the whole app (scripts allowed here)
    components.html(html, height=760, scrolling=True)


# Allow running as a page
if __name__ == "__main__":
    run()
