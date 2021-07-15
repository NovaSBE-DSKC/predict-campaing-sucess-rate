
from dskc import dskc_graphs

def get_channel(df, projects_df):
    channels = []
    channels_uncond = ["PPL Causas",
                       "WACT"
                       "Fundão Funding",
                       "Tempos Brilhantes",
                       "Terra dos Sonhos",
                       "Maratona da Saúde",
                       "IES-SBS",
                       "Fundação EDP",
                       "Giving Tuesday"]

    cs=set()
    for index, row in df.iterrows():
        # channel
        channel = projects_df[projects_df["PID"] == row["PID"]]["CHANNEL"]

        is_in = False
        for i,item in channel.iteritems():
            item=item.strip()
            cs.add(item)
            if item.strip()=="":
                continue

            if item in channels_uncond:
                is_in = True
                break

        channels.append(is_in)

    return channels
