import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from django.conf import settings
from .models import Ticket

sns.set(style="whitegrid")
def generate_priority_dashboard():
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    qs = Ticket.objects.all().values(
        "ticket_id",  
        "priority",
        "status",
        "raised_at",
        "closed_at",
        "address",
        "subject"
    )

    df = pd.DataFrame(list(qs))

    if df.empty:
        return {}

   
    df["raised_at"] = pd.to_datetime(df["raised_at"], utc=True)
    df["closed_at"] = pd.to_datetime(df["closed_at"], utc=True)

   
    # Priority Heat
 

    total_by_priority = df.groupby("priority").size()
    open_df = df[df["status"] == "OPEN"]
    open_by_priority = open_df.groupby("priority").size()

    heat_percent = (open_by_priority / total_by_priority * 100).fillna(0)

    plt.figure(figsize=(6,4))
    heat_percent.plot(kind="bar")
    plt.title("Open Ticket % by Priority")
    plt.ylabel("Percentage")
    plt.tight_layout()
    plt.savefig(os.path.join(settings.MEDIA_ROOT, "priority_heat.png"))
    plt.close()

  
    # AVG Resolution by Priority
  

    resolved_df = df[df["closed_at"].notna()].copy()

    if not resolved_df.empty:
        resolved_df["resolution_hours"] = (
            (resolved_df["closed_at"] - resolved_df["raised_at"])
            .dt.total_seconds() / 3600
        )

        avg_resolution = resolved_df.groupby("priority")["resolution_hours"].mean()

        plt.figure(figsize=(6,4))
        avg_resolution.plot(kind="bar")
        plt.title("Average Resolution Time (Hours)")
        plt.ylabel("Hours")
        plt.tight_layout()
        plt.savefig(os.path.join(settings.MEDIA_ROOT, "avg_resolution.png"))
        plt.close()

        avg_path = True
    else:
        avg_path = False

   
    #  Escalation Risk
    threshold_hours = 24
    p1_open = open_df[open_df["priority"] == "P1"].copy()

    risk_percent = 0

    if not p1_open.empty:
        p1_open["open_hours"] = (
            (pd.Timestamp.now(tz="UTC") - p1_open["raised_at"])
            .dt.total_seconds() / 3600
        )

        risky = p1_open[p1_open["open_hours"] > threshold_hours]
        risk_percent = (len(risky) / len(p1_open)) * 100

    plt.figure(figsize=(6,4))
    plt.bar(["Escalation Risk"], [risk_percent])
    plt.ylim(0,100)
    plt.title("P1 Open > 24h (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(settings.MEDIA_ROOT, "risk_meter.png"))
    plt.close()

    red_alert = risk_percent > 30


    # CITY ANALYTICS
 

    df["resolution_hours"] = np.where(
        df["closed_at"].notna(),
        (df["closed_at"] - df["raised_at"]).dt.total_seconds() / 3600,
        np.nan
    )

    city_stats = df.groupby("address").agg(
        total_tickets=("ticket_id", "count"),
        closed_tickets=("closed_at", lambda x: x.notna().sum()),
        avg_resolution=("resolution_hours", "mean")
    ).reset_index()

   
    #  Top 5 Problem Cities
   

    top5 = city_stats.sort_values(
        by="total_tickets",
        ascending=False
    ).head(5)

    plt.figure(figsize=(6,4))
    plt.bar(top5["address"], top5["total_tickets"])
    plt.xticks(rotation=45)
    plt.title("Top 5 Problem Cities")
    plt.tight_layout()
    plt.savefig(os.path.join(settings.MEDIA_ROOT, "top5_cities.png"))
    plt.close()

    
    #  Fastest & Slowest City
   

    resolved_cities = city_stats.dropna(subset=["avg_resolution"])

    if not resolved_cities.empty:
        fastest_city = resolved_cities.loc[
            resolved_cities["avg_resolution"].idxmin()
        ]["address"]

        slowest_city = resolved_cities.loc[
            resolved_cities["avg_resolution"].idxmax()
        ]["address"]
    else:
        fastest_city = "N/A"
        slowest_city = "N/A"

  
    # City Performance Score
   

    city_stats["performance_score"] = np.where(
      city_stats["avg_resolution"].notna(),
      (city_stats["closed_tickets"] / city_stats["total_tickets"]) *
      (1 / city_stats["avg_resolution"]),
      0
  )

    leaderboard = city_stats[ city_stats["performance_score"] > 0
    ].sort_values(
        by="performance_score",
        ascending=False
    )
    if not leaderboard.empty:
      plt.figure(figsize=(6,4))
      plt.bar(leaderboard["address"], leaderboard["performance_score"])
      plt.xticks(rotation=45)
      plt.title("City Performance Leaderboard")
      plt.tight_layout()
      plt.savefig(os.path.join(settings.MEDIA_ROOT, "city_leaderboard.png"))
      plt.close()

    # Clean subject text
    df["subject_clean"] = df["subject"].str.lower()

    # Count most common subjects
    top_subjects = (
        df["subject_clean"]
        .value_counts()
        .head(5)
    )
    plt.figure(figsize=(6,4))
    plt.bar(top_subjects.index, top_subjects.values)
    plt.xticks(rotation=45)
    plt.title("Top Recurring Problems")
    plt.tight_layout()
    plt.savefig(os.path.join(settings.MEDIA_ROOT, "top_subjects.png"))
    plt.close()

    def classify_issue(subject):
        subject = subject.lower()
        
        if any(word in subject for word in ["delay", "late", "delivery"]):
            return "Delivery Issues"
        elif any(word in subject for word in ["stock", "inventory", "out of stock"]):
            return "Inventory Issues"
        elif any(word in subject for word in ["damaged", "wrong item", "defective"]):
            return "Product Issues"
        elif any(word in subject for word in ["shipping", "courier", "tracking"]):
            return "Shipping Issues"
        else:
            return "Other"
    df["issue_cluster"] = df["subject"].apply(classify_issue)
    cluster_counts = df["issue_cluster"].value_counts()

    plt.figure(figsize=(6,4))
    plt.pie(
        cluster_counts,
        labels=cluster_counts.index,
        autopct="%1.1f%%"
    )
    plt.title("Cluster-wise Ticket Share")
    plt.tight_layout()
    plt.savefig(os.path.join(settings.MEDIA_ROOT, "cluster_share.png"))
    plt.close()


    
    return {
        "heat_chart": settings.MEDIA_URL + "priority_heat.png",
        "avg_chart": settings.MEDIA_URL + "avg_resolution.png" if avg_path else None,
        "risk_chart": settings.MEDIA_URL + "risk_meter.png",
        "risk_percent": round(risk_percent, 2),
        "red_alert": red_alert,
        "fastest_city": fastest_city,
        "slowest_city": slowest_city,
        "top5_chart": settings.MEDIA_URL + "top5_cities.png",
        "leaderboard_chart": settings.MEDIA_URL + "city_leaderboard.png",
        "top_subjects_chart": settings.MEDIA_URL + "top_subjects.png",
        "cluster_chart": settings.MEDIA_URL + "cluster_share.png",
    }