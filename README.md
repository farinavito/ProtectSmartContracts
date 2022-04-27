# ProtectSmartContracts
A way to reduce the risk in smart contracts when one address is compromised

#VISUAL REPRESENTATION

    protector 1 ---|
		protector 2 ---|
		protector 3 ---|----- protectorWaitingToBeOwner ---------- protectorOwner------------------------whitelistedAdresses
		protector 4 ---|      (can only change owner)     (can only add or removed from whitelist)       (do day to day jobs)
		protector 5 ---|

